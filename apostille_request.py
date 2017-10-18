#!/usr/bin/env python3
import json
import os
import requests
from bs4 import BeautifulSoup

dogm_url = 'https://dogm-1-trp.mos.ru/Search'

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

def main():
    entries = read_entries('entries.json')
    for entry in entries['entry']:
        payload = {
                'RegNumber': entry['reg_num'],
                'HolderLastName': entry['last_name'],
                'HolderFirstName': entry['first_name']
        }
        r = requests.get(dogm_url, data=payload)
        page = r.text
        soup = BeautifulSoup(page, 'html.parser')
        status = soup.find('h4')
        print(entry['reg_num'] + ': ' + status.string)


if __name__ == '__main__':
    main()
