import hashlib
import unittest

from tests.base_test import BaseTestCase
from app.models.user import User
from app.models.task import Task
from app.models.comment import Comment
from app.models.base import db


class TestComments(BaseTestCase):

    ENDPOINT = 'api/tasks'

    def test_get_comments_no_auth(self):
        self.assert401(self.client.get(self.ENDPOINT))

    def test_get_comments_for_not_existing_task(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '/1/comments',
                              headers={'token': token})
        self.assert403(res)

    def test_get_comments_for_not_assigned_task(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        comment1 = Comment(text='yey', user_id=1, task_id=1)
        db.session.add(task1)
        db.session.add(comment1)
        db.session.commit()
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.get(self.ENDPOINT + '/1/comments',
                              headers={'token': token})
        self.assert403(res)

    def test_get_comments_for_assigned_task(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        comment1 = Comment(text='yey', user_id=1, task_id=1)
        db.session.add(task1)
        db.session.add(comment1)
        db.session.commit()
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '/1/comments',
                              headers={'token': token})
        self.assert200(res)
        self.assertDictEqual(res.json[0], {'text': 'yey',
                                           'user_id': 1})
        self.assertEqual(len(res.json), 1)

    def test_post_comments_for_not_assigned_task(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        comment1 = Comment(text='yey', user_id=1, task_id=1)
        db.session.add(task1)
        db.session.add(comment1)
        db.session.commit()
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.post('api/tasks/1/comments',
                               headers={'token': token},
                               data={'text': 'yey'})
        self.assertEqual(res.status_code, 403)

    def test_post_comments_with_no_text(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        token = self.login().json['token']
        res = self.client.post('api/tasks/1/comments',
                               headers={'token': token},
                               data={'not_text': 'yey'})
        self.assertEqual(res.status_code, 400)

    def test_post_comments_for_assigned_task(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        token = self.login().json['token']
        res = self.client.post('api/tasks/1/comments',
                               headers={'token': token},
                               data={'text': 'yey'})
        self.assertEqual(res.status_code, 201)
        res = self.client.get('api/tasks/1/comments',
                              headers={'token': token})
        self.assertDictEqual(res.json[0], {'text': 'yey', 'user_id': 1})
        comment = Comment.query.get(1)
        self.assertEqual(comment.text, 'yey')
        self.assertEqual(comment.user_id, 1)
        self.assertEqual(comment.task_id, 1)

    def test_post_comments_for_assigned_task_form_data(self):
        task1 = Task(title='title1', status='in_progress')
        task1.assign_user(1)
        db.session.add(task1)
        db.session.commit()
        token = self.login().json['token']
        res = self.client.post('api/tasks/1/comments',
                               headers={'token': token},
                               data={'text': 'yey'},
                               content_type='multipart/form-data')
        self.assertEqual(res.status_code, 201)
        res = self.client.get('api/tasks/1/comments',
                              headers={'token': token})
        self.assertDictEqual(res.json[0], {'text': 'yey', 'user_id': 1})
        comment = Comment.query.get(1)
        self.assertEqual(comment.text, 'yey')
        self.assertEqual(comment.user_id, 1)
        self.assertEqual(comment.task_id, 1)


if __name__ == '__main__':
    unittest.main()
