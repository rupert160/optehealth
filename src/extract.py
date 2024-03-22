#!/usr/bin/env python3

import requests, os, pathlib

test_file = './test.html'
test_uri = 'https://www.fao.org/3/AC854T/AC854T03.htm'

def pull_test_file(uri:str, output_file:str):
    r = requests.get(uri,output_file)
    r.status_code
    with open(test_file,'w') as tw:
        tw.write(r.text)

def main():
    if not os.path.isfile(test_file):
        pull_test_file(test_uri, test_file)


if __name__ == '__main__':
    main()