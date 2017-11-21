#!/usr/bin/env python3
import json
import os
import requests
from bs4 import BeautifulSoup
from enum import Enum

def read_entries(filename):
    try:
        with open(filename, 'r') as f:
            apostilles = json.load(f)
            return apostilles
    except FileNotFoundError:
            print('Cannot find entries file \'', filename, '\'')
    except json.JSONDecodeError as e:
            print('Cannot parse JSON-file: ', str(e))
    return None

class ApostilleStatus(Enum):
    UNKNOWN = 0
    NOT_FOUND = 1
    NOT_READY = 2
    READY = 3

class ApostilleChecker():
    dogm_url = 'https://dogm-1-trp.mos.ru/Search'

    def __init__(self, entry):
        self.payload = {
                'RegNumber': entry['reg_num'],
                'HolderLastName': entry['last_name'],
                'HolderFirstName': entry['first_name']
        }
        self.status = (ApostilleStatus.UNKNOWN, 'Нет данных')


    def __str__(self):
        return "{0}: {1}".format(self.payload['RegNumber'], self.status[1])


    def _response_to_status(self, response):
        known_responses = {
                "Ваш апостиль готов": ApostilleStatus.READY,
                "Документ принят к рассмотрению. Заявление находится в работе":
                ApostilleStatus.NOT_READY,
                "Ничего не найдено": ApostilleStatus.NOT_FOUND
        }
        return known_responses.get(response, ApostilleStatus.UNKNOWN)

    def request_status(self):
        r = requests.get(self.dogm_url, data=self.payload)
        page = r.text
        soup = BeautifulSoup(page, 'html.parser')
        
        # there are no ids or anything useful to track down needed info
        # so we have to search for the only <h4></h4> header tag present
        # on that page
        response = soup.find('h4').string
        self.status = (self._response_to_status(response), response)
        return self.status


def main():
    entries = read_entries('entries.json')
    for entry in entries['entry']:
        checker = ApostilleChecker(entry)
        checker.request_status()
        print(checker)


if __name__ == '__main__':
    main()
