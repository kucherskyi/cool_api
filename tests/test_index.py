#! env/bin/python

import json
import unittest

from tests.base_test import BaseTestCase


class TestIndex(BaseTestCase):

    def test_no_token(self):
        response = self.client.get('/api/index')
        self.assertEqual(response.status_code, 401)

    def test_empty_token(self):
        response = self.client.get('/api/index', headers={'token': ''})
        self.assertEqual(response.status_code, 401)

    def test_inv_token(self):
        token = self.login().json['token'] + '1'
        response = self.client.get('/api/index', headers={'token': token})
        self.assertEqual(response.status_code, 401)

    def test_token(self):
        token = self.login().json['token']
        response = self.client.get('/api/index', headers={'token': token})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
