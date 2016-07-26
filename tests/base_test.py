from base64 import b64encode
from flask import current_app
from flask_testing import TestCase
import hashlib

from app.app import create_app
from app.models.user import User, db


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        current_app.config['TESTING'] = True
        current_app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql://admin:pass@localhost:5432/test'
        db.create_all()
        user1 = User(name='user1', email='email1@em.co')
        user1.password = hashlib.md5('pass1').hexdigest()
        db.session.add(user1)
        db.session.commit()
        self.token = user1.generate_auth_token()
        self.client = current_app.test_client()
        self.auth_header = {'token': self.token}

    def login(self, name='user1', password='pass1'):
        credentials = b64encode("{}:{}".format(name, password))
        headers = {'Authorization': 'Basic ' + credentials}
        return self.client.get("/api/login",
                               headers=headers,
                               follow_redirects=True)

    def logged_in_user(self):
        token = self.login().json['token']
        response = self.client.get('/api/users', headers={'token': token})
        return response

    def tearDown(self):
        db.session.remove()
        db.drop_all()
