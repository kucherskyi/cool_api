#! env/bin/python

import json
import unittest

from tests.base_test import BaseTestCase


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
        response = self.client.post('/api/users',
                                    headers={'token': token},
                                    data={"email": "email1"})
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


class TestGetSingleUser(BaseTestCase):

    def test_get_single_user_with_no_token(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user = self.client.get('/api/users/' + str(user))
        self.assertEqual(single_user.status_code, 401)

    def test_get_single_user_with_invalid_token(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        token = self.login().json['token'] + '1'
        single_user = self.client.get('/api/users/' + str(user),
                                      headers={'token': token})
        self.assertEqual(single_user.status_code, 401)

    def test_get_single_user_with_no_id(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        single_user = self.client.get('/api/users/', headers={'token': token})
        self.assertEqual(single_user.status_code, 404)

    def test_get_single_user_with_invalid_id(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)
        for item in user:
            max_id = 1
            if item['id'] > max_id:
                max_id = item['id']
        single_user = self.client.get('/api/users/' + str(max_id + 1),
                                      headers={'token': token})
        self.assertEqual(single_user.status_code, 404)

    def test_get_single_user(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user = self.client.get('/api/users/' + str(user),
                                      headers={'token': token})
        self.assertEqual(single_user.status_code, 200)


class TestDeleteUser(BaseTestCase):

    def test_delete_single_user_with_no_token(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user = self.client.delete('/api/users/' + str(user))
        self.assertEqual(single_user.status_code, 401)

    def test_delete_single_user_with_invalid_token(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        token = self.login().json['token'] + '1'
        single_user = self.client.delete('/api/users/' + str(user),
                                         headers={'token': token})
        self.assertEqual(single_user.status_code, 401)

    def test_delete_single_user_with_no_id(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        single_user = self.client.get('/api/users/', headers={'token': token})
        self.assertEqual(single_user.status_code, 404)

    def test_delete_single_user_with_invalid_id(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)
        for item in user:
            max_id = 1
            if item['id'] > max_id:
                max_id = item['id']
        single_user = self.client.delete('/api/users/' + str(max_id + 1),
                                         headers={'token': token})
        self.assertEqual(single_user.status_code, 400)

    def test_delete_single_user(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user = self.client.delete('/api/users/' + str(user),
                                         headers={'token': token})
        self.assertEqual(single_user.status_code, 204)
        return user

    def test_user_is_deleted(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = self.test_delete_single_user()
        single_user = self.client.get('/api/users/' + str(user),
                                      headers={'token': token})
        self.assertEqual(single_user.status_code, 401)


class TestPutUser(BaseTestCase):

    def test_put_single_user_with_no_token(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user_info = self.client.get('/api/users/' + str(user),
                                           headers={'token': token})
        info = json.loads(single_user_info.data)['info']
        update_user = self.client.put('/api/users/' + str(user),
                                      data={"info": str(info) + 'udpated'})
        self.assertEqual(update_user.status_code, 401)

    def test_put_single_user_with_invalid_token(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user_info = self.client.get('/api/users/' + str(user),
                                           headers={'token': token})
        info = json.loads(single_user_info.data)['info']
        token = self.login().json['token'] + '1'
        update_user = self.client.put('/api/users/' + str(user),
                                      headers={'token': token},
                                      data={"info": str(info) + 'udpated'})
        self.assertEqual(update_user.status_code, 401)

    def test_put_single_user_with_no_id(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user_info = self.client.get('/api/users/' + str(user),
                                           headers={'token': token})
        info = json.loads(single_user_info.data)['info']
        single_user = self.client.put('/api/users/',
                                      headers={'token': token},
                                      data={"info": str(info) + 'updated'})
        self.assertEqual(single_user.status_code, 404)

    def test_put_single_user(self):
        token = self.login().json['token']
        all_us = self.client.get('/api/users', headers={'token': token})
        user = json.loads(all_us.data)[0]['id']
        single_user_info = self.client.get('/api/users/' + str(user),
                                           headers={'token': token})
        info = json.loads(single_user_info.data)['info']
        update_user = self.client.put('/api/users/' + str(user),
                                      headers={'token': token},
                                      data={"info": str(info) + 'udpated'})
        self.assertEqual(update_user.status_code, 201)
        updated_info = json.loads(update_user.data)['info']
        self.assertNotEqual(info, updated_info)


if __name__ == '__main__':
    unittest.main()
