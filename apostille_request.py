#!/usr/bin/env python3
import json
import os
import requests
from bs4 import BeautifulSoup

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

class ApostilleChecker():
    dogm_url = 'https://dogm-1-trp.mos.ru/Search'

    def __init__(self, entry):
        self.payload = {
                'RegNumber': entry['reg_num'],
                'HolderLastName': entry['last_name'],
                'HolderFirstName': entry['first_name']
        }
        self.status = None

    def __str__(self):
        return "{0}: {1}".format(self.payload['RegNumber'], self.status)


    def update_status(self):
        r = requests.get(self.dogm_url, data=self.payload)
        page = r.text
        soup = BeautifulSoup(page, 'html.parser')
        
        # there are no ids or anything useful to track down needed info
        # so we have to search for the only <h4></h4> header tag present
        # on that page
        self.status = soup.find('h4').string
        return self.status


def main():
    entries = read_entries('entries.json')
    for entry in entries['entry']:
        checker = ApostilleChecker(entry)
        checker.update_status()
        print(checker)


if __name__ == '__main__':
    main()
