#! env/bin/python

from flask_restful import reqparse
import json
import hashlib
import unittest

from app.models.user import User, db
from app.controllers.parsers import post_user
from tests.base_test import BaseTestCase

post_user = reqparse.RequestParser()
post_user.add_argument('name', type=str, required=True)
post_user.add_argument('password', type=str, required=True)
post_user.add_argument('email', type=str, required=True)


class TestGetAllUsers(BaseTestCase):

    def test_get_users_with_no_token(self):
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 401)

    def test_get_users_with_empty_token(self):
        response = self.client.get('/api/users', headers={'token': ''})
        self.assertEqual(response.status_code, 401)

    def test_get_users_with_invalid_token(self):
        token = self.login().json['token'] + '1'
        response = self.client.get('/api/users', headers={'token': token})
        self.assertEqual(response.status_code, 401)

    def test_get_users_with_valid_token(self):
        token = self.login().json['token']
        response = self.client.get('/api/users', headers={'token': token})
        self.assertEqual(response.status_code, 200)

    def test_response_contains_users(self):
        token = self.login().json['token']
        response = self.client.get('/api/users', headers={'token': token})
        self.assertEqual(json.loads(response.data)[0]["name"], "user1")


class TestPostUser(BaseTestCase):

    def test_post_user_with_no_token(self):
        response = self.client.post('/api/users')
        self.assertEqual(response.status_code, 401)

    def test_gpost_users_with_empty_token(self):
        response = self.client.post('/api/users', headers={'token': ''})
        self.assertEqual(response.status_code, 401)

    def test_post_users_with_invalid_token(self):
        token = self.login().json['token'] + '1'
        response = self.client.post(
            '/api/users', headers={'token': token}, data={"name": "name"})
        self.assertEqual(response.status_code, 401)

    def test_post_user_with_taken_email(self):
        token = self.login().json['token']
        response = self.client.post(
            '/api/users', headers={'token': token}, data={"email": "email1"})
        self.assertEqual(response.status_code, 400)

    def test_valid_post_user(self):
        new_user = {
            "name": "name1",
            "password": "pass1",
            "email": "email321",
            "is_admin": "0"
        }
        token = self.login().json['token']
        response = self.client.post('/api/users',
                                    headers={'token': token},
                                    data=new_user)
        self.assertEqual(response.status_code, 201)
        new_user["password"] = "pass1"
        return new_user

    def test_created_user_able_to_login(self):
        created_user = self.test_valid_post_user()
        self.assertEqual(self.login(created_user['name'],
                                    created_user['password']).status_code, 200)


if __name__ == '__main__':
    unittest.main()
