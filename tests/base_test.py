#! env/bin/python

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
        current_app.config['WTF_CSRF_ENABLED'] = False
        current_app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql://admin:pass@localhost:5432/test'
        current_app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        db.create_all()
        user1 = User(name='user1', email = 'email1')
        user1.password = hashlib.md5('pass1').hexdigest()
        db.session.add(user1)
        db.session.commit()
        self.client = current_app.test_client()

    def login(self, name='user1', password='pass1'):
        credentials = b64encode("{}:{}".format(name, password))
        headers = {'Authorization': 'Basic ' + credentials}
        return self.client.get("/api/login",
                               headers=headers,
                               follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
