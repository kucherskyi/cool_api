import hashlib
import unittest
import mock

from tests.base_test import BaseTestCase
from app.models.user import User
from app.models.task import Task
from app.models.comment import Comment
from app.models.base import db


class TestUsersReport(BaseTestCase):

    ENDPOINT = 'api/reports/user_comments'

    def test_get_report_no_auth(self):
        self.assert401(self.client.get(self.ENDPOINT))

    def test_get_report_no_admin(self):
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.get('api/tasks/1/comments',
                               headers={'token': token})

    def test_get_report_admin_wrong_format(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT+ '?format=not_valid',
                              headers={'token': token})
        self.assert400(res)

    def test_get_report_no_format(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT,
                              headers={'token': token})
        self.assertEqual(res.status_code, 200)


    def test_get_report_json(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT+'?format=json',
                              headers={'token': token})
        self.assertEqual(res.status_code, 200)

    def test_get_report_csv(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        comment1 = Comment(text='yey', user_id=1, task_id=1)
        db.session.add(task1)
        db.session.add(comment1)
        db.session.commit()
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=csv',
                              headers={'token': token})
        self.assertEqual(res.status_code, 200)

    def test_get_report_pdf(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        comment1 = Comment(text='yey', user_id=1, task_id=1)
        db.session.add(task1)
        db.session.add(comment1)
        db.session.commit()
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT+'?format=pdf',
                              headers={'token': token})
        self.assertEqual(res.status_code, 200)

class TestTasksReport(BaseTestCase):

    ENDPOINT = 'api/reports/task_stats'

    def test_get_report_no_auth(self):
        self.assert401(self.client.get(self.ENDPOINT))

    def test_get_report_no_admin(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT+ '?format=not_valid',
                              headers={'token': token})
        self.assert400(res)

    def test_get_report_wrong_format(self):
        pass

    def test_get_report_no_format(self):
        pass

    def test_get_report_json(self):
        pass

    def test_get_report_if_data_valid(self):
        pass

    def test_get_report_csv(self):
        pass

    def test_get_report_pdf(self):
        pass


if __name__ == '__main__':
    unittest.main()
