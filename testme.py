#!/usr/bin/python3
""" unitest for user input API """
import json
import unittest
import pep8
from v1.app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """setup application"""
        self.app = app.test_client()

    def test_index(self):
        """get index"""
        rv = self.app.get('/')

    def test_not_found(self):
        """test not found 404"""
        rv = self.app.get('/nopath')
        self.assertEqual(rv.status_code, 404,
                         "there is no path here")

    def test_without_json_request(self):
        """Test the request is it json or not"""
        response = self.app.post('/v1/sanitized/input', data=json.dumps({
            'payload': '1\''}))
        self.assertEqual(response.status_code, 400,
                         "json request")
        self.assertEqual(response.json['error'], 'Not a JSON',
                         "ther is no error")

    def test_without_payload_input(self):
        """Test the request without input"""
        response = self.app.post('/v1/sanitized/input', data=json.dumps({
            'nopayload': '1\''}), content_type='application/json')
        self.assertEqual(response.status_code, 400,
                         "ther is no error")
        self.assertEqual(response.json['error'], 'Missing input',
                         "ther is no error")

    def test_without_sqlpattern(self):
        """Test the request without sql pattern"""
        response = self.app.post('/v1/sanitized/input', data=json.dumps({
            'payload': '1'}), content_type='application/json')
        self.assertEqual(response.json["result"], "sanitized",
                         "there is an sqli pattern")

    def test_with_sqlpattern(self):
        """Test the request with an sql pattern"""
        response = self.app.post('/v1/sanitized/input', data=json.dumps({
            'payload': '1\''}), content_type='application/json')
        self.assertEqual(response.json["result"], "unsanitized",
                         "there is no sqli pattern")




if __name__ == '__main__':
     unittest.main()

