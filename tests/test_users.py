import json
import unittest
import hashlib

from tests.base_test import BaseTestCase
from app.models.user import db, User


class TestUserList(BaseTestCase):
    ENDPOINT = 'api/users'
    REQUIRED_DATA = {
        'name': 'name4',
        'password': '1',
        'email': 'email4'
    }

    def test_get_no_auth(self):
        self.assert401(self.client.get(self.ENDPOINT))

    def test_get_users_count(self):
        res = self.client.get(self.ENDPOINT, headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(len(res.json), 1)
        user2 = User(name='user2', email='email2', password='1')
        user3 = User(name='user3', email='email3', password='1')
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        res = self.client.get(self.ENDPOINT, headers=self.auth_header)
        self.assertEqual(len(res.json), 3)

    def test_get_user_fields(self):
        res = self.client.get(self.ENDPOINT, headers=self.auth_header)
        self.assertDictEqual(res.json[0], {'name': 'user1', 'id': 1})

    def test_post_no_required(self):
        for key in self.REQUIRED_DATA.keys():
            params = self.REQUIRED_DATA.copy()
            del params[key]
            self.assert400(self.client.post(self.ENDPOINT,
                                            headers=self.auth_header,
                                            data=params))

    def test_post_all_field(self):
        params = self.REQUIRED_DATA.copy()
        params['info'] = 'test info'
        params['is_admin'] = False

        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assertEqual(res.status_code, 201)
        self.assertDictEqual(res.json, {'id': 2})

        user = User.query.get(2)
        self.assertEqual(user.name, 'name4')
        self.assertEqual(user.email, 'email4')
        self.assertEqual(user.info, 'test info')
        self.assertEqual(user.password, hashlib.md5('1').hexdigest())
        self.assertEqual(user.is_admin, False)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_post_default_fields(self):
        params = self.REQUIRED_DATA.copy()
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assertEqual(res.status_code, 201)
        self.assertDictEqual(res.json, {'id': 2})
        user = User.query.get(2)
        self.assertEqual(user.is_admin, False)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_post_data_error(self):
        params = self.REQUIRED_DATA.copy()
        params['name'] = 'user1' * 100
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assert400(res)
        self.assertIn('DataError', res.json['message'])

    def test_post_integrity_error(self):
        params = self.REQUIRED_DATA.copy()
        params['name'] = 'user1'
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assert400(res)
        self.assertIn('IntegrityError', res.json['message'])

        params = self.REQUIRED_DATA.copy()
        params['email'] = 'email1'
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assert400(res)
        self.assertIn('IntegrityError', res.json['message'])


class TestUserSingle(BaseTestCase):
    ENDPOINT = 'api/users'

    def test_get_not_found(self):
        res = self.client.get(self.ENDPOINT + '/100', headers=self.auth_header)
        self.assert404(res)
        user = User.query.get(100)
        self.assertEqual(user, None)

    def test_get(self):
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        self.assertIn('user1', res.json['name'])
        self.assertIn('email1', res.json['email'])
        self.assertEqual(res.json['info'], None)
        self.assertEqual(res.json['is_admin'], False)
        self.assertIn('2016', res.json['created_at'])
        self.assertIn('2016', res.json['updated_at'])

    def test_delete_user(self):
        user2 = User(name='user2', email='email2', password='1')
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(User.query.count(), 2)
        res = self.client.delete(self.ENDPOINT + '/2',
                                 headers=self.auth_header)
        self.assertEqual(res.status_code, 204)
        res = self.client.get(self.ENDPOINT + '/2',
                              headers=self.auth_header)
        self.assert404(res)
        self.assertEqual(User.query.count(), 1)

    def test_put_user_with_no_info(self):
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(res.json['info'], None)
        self.assertEqual(User.query.get(1).info, None)
        res = self.client.put(self.ENDPOINT + '/1',
                              headers=self.auth_header)
        self.assert400(res)
        self.assertEqual(User.query.get(1).info, None)

    def test_put_user(self):
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(res.json['info'], None)
        self.assertEqual(User.query.get(1).info, None)
        res = self.client.put(self.ENDPOINT + '/1',
                              headers=self.auth_header,
                              data={'info': 'updated'})
        self.assert200(res)
        self.assertEqual(res.json['info'], 'updated')
        self.assertEqual(User.query.get(1).info, 'updated')

if __name__ == '__main__':
    unittest.main()
