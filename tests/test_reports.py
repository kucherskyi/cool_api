from flask import current_app
import hashlib
import unittest
import mock

from tests.base_test import BaseTestCase
from app.models.user import User
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
        res = self.client.get('api/tasks/1/comments', headers={'token': token})
        self.assert403(res)

    def test_get_report_admin_wrong_format(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=not_valid',
                              headers={'token': token})
        self.assert400(res)

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_no_format(self, mock_email, mock_format):
        mock_json = mock_format.get('json', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT, headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter='|',
                                          emplate='/report_comments.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'application/json')

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_json(self, mock_email, mock_format):
        mock_json = mock_format.get('json', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=json',
                              headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter='|',
                                          emplate='/report_comments.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'application/json')

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_csv(self, mock_email, mock_format):
        mock_json = mock_format.get('csv', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=csv',
                              headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter='|',
                                          emplate='/report_comments.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'text/csv')

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_pdf(self, mock_email, mock_format):
        mock_json = mock_format.get('csv', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=pdf',
                              headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter='|',
                                          emplate='/report_comments.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'application/pdf')


class TestTasksReport(BaseTestCase):

    ENDPOINT = 'api/reports/task_stats'

    def test_get_report_no_auth(self):
        self.assert401(self.client.get(self.ENDPOINT))

    def test_get_report_no_admin(self):
        user2 = User(name='user2', email='email2@em.co')
        user2.password = hashlib.md5('1').hexdigest()
        db.session.add(user2)
        db.session.commit()
        token = self.login('user2', '1').json['token']
        res = self.client.get('api/tasks/1/comments', headers={'token': token})
        self.assert403(res)

    def test_get_report_admin_wrong_format(self):
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=not_valid',
                              headers={'token': token})
        self.assert400(res)

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_no_format(self, mock_email, mock_format):
        mock_json = mock_format.get('json', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT, headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter=',',
                                          emplate='/report_tasks.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'application/json')

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_json(self, mock_email, mock_format):
        mock_json = mock_format.get('json', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=json',
                              headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter=',',
                                          emplate='/report_tasks.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'application/json')

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_csv(self, mock_email, mock_format):
        mock_json = mock_format.get('csv', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=csv',
                              headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter=',',
                                          emplate='/report_tasks.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'text/csv')

    @mock.patch('app.controllers.reports.FORMAT_FUNC')
    @mock.patch('app.email_sender.send_mail')
    def test_get_report_pdf(self, mock_email, mock_format):
        mock_json = mock_format.get('csv', return_value=mock.MagicMock())
        token = self.login().json['token']
        res = self.client.get(self.ENDPOINT + '?format=pdf',
                              headers={'token': token})
        self.assert200(res)
        mock_json.assert_called_once_with([], delimiter=',',
                                          emplate='/report_tasks.html',
                                          indent=4)
        mock_email.assert_called_once_with(current_app,
                                           mock_json.return_value,
                                           'application/pdf')


if __name__ == '__main__':
    unittest.main()
