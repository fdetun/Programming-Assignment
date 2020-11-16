#!/usr/bin/python3
""" unitest for user input API """
import json
import unittest
import requests
import pep8

URL = "http://0.0.0.0:5006/v1/sanitized/input/"
injectionpattern = input("Please write your sql injection pattern : ")
simplepattern = input("Please write your  simple input : ")


class TestFunctions(unittest.TestCase):

    def test_pep8(self):
        """Test that sqlapi.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['v1/sanitized/sqlapi.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_request_not_json(self):
        """Test the request is it json or not"""
        r = requests.request("POST", URL)
        self.assertEqual(r.status_code, 400,
                         "ther is no error")
        self.assertEqual(r.json()['error'], 'Not a JSON',
                         "ther is no error")

    def test_request_no_input(self):
        """Test if there is an input or not"""
        headers = {'Content-Type': 'application/json'}
        r = requests.request("POST", URL, headers=headers,
                             data="{\"noinput\": \"noinput\"}")
        self.assertEqual(r.status_code, 400,
                         "ther is no error")
        self.assertEqual(r.json()['error'], 'Missing input',
                         "ther is no error")

    def test_request_with_injection_patterns(self):
        """test request with a unsanitized pattern"""
        payload = '{"payload": "' + injectionpattern + "\"}"
        headers = {'Content-Type': 'application/json'}
        r = requests.request("POST", URL, headers=headers, data=payload)
        self.assertEqual(r.status_code, 406,
                         "there is an sql injection pattern")
        self.assertEqual(r.json()['result'], 'unsanitized',
                         "there is an sql injection pattern")

    def test_request_with_injection_patterns(self):
        payload = '{"payload": "' + simplepattern + "\"}"
        headers = {'Content-Type': 'application/json'}
        r = requests.request("POST", URL, headers=headers, data=payload)
        self.assertEqual(r.status_code, 200,
                         "there is no injection pattern")
        self.assertEqual(r.json()['result'], 'sanitized',
                         "there is no injection pattern")

    def test_not_found_path(self):
        """test request with a sanitized pattern"""
        headers = {'Content-Type': 'application/json'}
        r = requests.request("GET", "http://0.0.0.0:5006/test")
        self.assertEqual(r.status_code, 404,
                         "there is a path here")
        self.assertEqual(r.json()['error'], 'Not found',
                         "there is a path here")


if __name__ == '__main__':
    unittest.main()
