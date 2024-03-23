#!/usr/bin/env python3

import unittest, os, sys 
from bs4 import BeautifulSoup
from src.extract import pull_file as pf, get_next_page_uri

class TestExtract(unittest.TestCase):
    test_domain = 'https://www.fao.org/3/AC854T/'
    test_dir = '/tmp/'
    test_filename = 'AC854T03.htm'
    next_filename = 'AC854T04.htm'

    def test_pull_file(self):
        uri = self.test_domain + self.test_filename
        filepath = self.test_dir + self.test_filename
        pf(uri, filepath)
        self.assertTrue(os.stat(filepath).st_size > 0)

    def test_get_next_page_uri(self):
        uri = self.test_domain + self.test_filename
        filepath = self.test_dir + self.test_filename
        pf(uri, filepath)
        result_filename = get_next_page_uri(filepath)
        self.assertEqual(result_filename, self.next_filename)

# Run the tests
if __name__ == '__main__':
  unittest.main()