#! env/bin/python

from base64 import b64encode
import json
import hashlib
import unittest

from app.models.user import User, db
from base_test import BaseTestCase


class TestLogin(BaseTestCase):

    def test_login_with_no_auth(self):
        response = self.client.get("/api/login")
        self.assertEqual(response.status_code, 401)

    def test_login_with_invalid_credentials(self):
        response = self.login('aaa', 'aaa')
        self.assertEqual(response.status_code, 401)

    def test_login_with_other_credentials(self):
        user2 = User(name='user2')
        user2.password = hashlib.md5('pass2').hexdigest()
        db.session.add(user2)
        db.session.commit()
        response = self.login('user1', 'pass2')
        self.assertEqual(response.status_code, 401)

    def test_valid_login(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)

    def test_inv_token(self):
        user = User.verify_auth_token(self.login().json['token'] + '1')
        self.assertFalse(user)

    def test_token(self):
        user = User.verify_auth_token(self.login().json['token'])
        self.assertTrue(user)


if __name__ == '__main__':
    unittest.main()
