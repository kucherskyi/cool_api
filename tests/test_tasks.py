import json
import unittest
import hashlib

from tests.base_test import BaseTestCase
from app.models.user import db, User, Task, UserAndTaskRelation


class TestTasks(BaseTestCase):
    ENDPOINT = 'api/tasks'
    DATA = {
        'title': 'title1',
        'status': 'status1'
    }

    def test_get_no_auth(self):
        self.assert401(self.client.get(self.ENDPOINT))

    def test_get_tasks_count_for_other_user(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.get(self.ENDPOINT, headers={'token': token})
        self.assertEqual(len(res.json), 0)

    def test_get_tasks_count_for_current_user(self):
        res = self.client.get(self.ENDPOINT, headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(len(res.json), 0)
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        res = self.client.get(self.ENDPOINT, headers=self.auth_header)
        self.assertEqual(len(res.json), 1)

    def test_get_task_fields(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        res = self.client.get(self.ENDPOINT, headers=self.auth_header)
        self.assertDictEqual(res.json[0], {'title': 'title1',
                                           'status': 'status1',
                                           'id': 1,
                                           'users': '[1]'})

    def test_post_tasks_without_required(self):
        for key in self.DATA.keys():
            params = self.DATA.copy()
            del params[key]
            self.assert400(self.client.post(self.ENDPOINT,
                                            headers=self.auth_header,
                                            data=params))

    def test_post_task_data_error(self):
        params = self.DATA.copy()
        params['title'] = 'title1' * 50
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assert400(res)
        self.assertIn('DataError', res.json['message'])
        params = self.DATA.copy()
        params['status'] = 'status1' * 10
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=params)
        self.assert400(res)
        self.assertIn('DataError', res.json['message'])

    def test_post_task(self):
        res = self.client.post(self.ENDPOINT,
                               headers=self.auth_header,
                               data=self.DATA)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json['id'], 1)
        task = Task.query.get(1)
        self.assertEqual(task.title, 'title1')
        self.assertEqual(task.status, 'status1')
        self.assertEqual(str(task.users), '[1]')
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)


class TestTaskSingle(BaseTestCase):
    ENDPOINT = 'api/tasks'

    def test_get_not_found(self):
        res = self.client.get(self.ENDPOINT + '/100', headers=self.auth_header)
        self.assert404(res)
        task = Task.query.get(100)
        self.assertEqual(task, None)

    def test_get_forbidden(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.get(self.ENDPOINT + '/1', headers={'token': token})
        self.assert403(res)

    def test_get_assigned(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(res.json['id'], 1)
        self.assertEqual(res.json['status'], 'status1')
        self.assertEqual(res.json['title'], 'title1')
        self.assertEqual(res.json['users'], '[1]')
        self.assertIn('2016', res.json['created_at'])
        self.assertIn('2016', res.json['updated_at'])

    def test_delete_other_user_task(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        self.assertEqual(Task.query.count(), 1)
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.delete(self.ENDPOINT + '/1',
                                 headers={'token': token})
        self.assert403(res)
        self.assertEqual(Task.query.count(), 1)

    def test_delete_not_existing_task(self):
        task = Task.query.get(1)
        self.assertEqual(task, None)
        res = self.client.delete(self.ENDPOINT + '/1',
                                 headers=self.auth_header)
        self.assert404(res)

    def test_delete_task(self):
        task = Task(title='title1', status='status1')
        task.assign_user(1)
        db.session.add(task)
        db.session.commit()
        self.assertEqual(Task.query.count(), 1)
        res = self.client.delete(self.ENDPOINT + '/1',
                                 headers=self.auth_header)
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Task.query.count(), 0)

    def test_put_task_with_no_status(self):
        task = Task(title='title1', status='status1')
        task.assign_user(1)
        db.session.add(task)
        db.session.commit()
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(res.json['status'], 'status1')
        self.assertEqual(Task.query.get(1).status, 'status1')
        res = self.client.put(self.ENDPOINT + '/1',
                              headers=self.auth_header)
        self.assert400(res)
        self.assertEqual(Task.query.get(1).status, 'status1')

    def test_put_task_data_error(self):
        task = Task(title='title1', status='status1')
        task.assign_user(1)
        db.session.add(task)
        db.session.commit()
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        self.assertEqual(res.json['status'], 'status1')
        self.assertEqual(Task.query.get(1).status, 'status1')
        res = self.client.put(self.ENDPOINT + '/1',
                              headers=self.auth_header,
                              data={'status': 'statusstatusstatus'})
        self.assert400(res)
        self.assertEqual(Task.query.get(1).status, 'status1')

    def test_put_other_user_task(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        self.assertEqual(Task.query.get(1).status, 'status1')
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.put(self.ENDPOINT + '/1',
                              headers={'token': token},
                              data={'status': 'edited'})
        self.assert403(res)
        self.assertEqual(Task.query.get(1).status, 'status1')

    def test_put_user_task(self):
        task1 = Task(title='title1', status='status1')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        self.assertEqual(Task.query.get(1).status, 'status1')
        res = self.client.get(self.ENDPOINT + '/1', headers=self.auth_header)
        self.assert200(res)
        res = self.client.put(self.ENDPOINT + '/1',
                              headers=self.auth_header,
                              data={'status': 'edited'})
        self.assert200(res)
        self.assertEqual(Task.query.get(1).status, 'edited')

class TestAssignTask(BaseTestCase):

    ENDPOINT = 'api/assign_task'

    def test_post_assign_no_auth(self):
        res = self.client.post(self.ENDPOINT)
        self.assert401(res)

if __name__ == '__main__':
    unittest.main()
