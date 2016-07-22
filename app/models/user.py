#!env/bin/python

from flask import current_app
import hashlib
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint

from base import Base, db


class User(Base):
    __tablename__ = 'users'
    name = Column(String(32), unique=True)
    password = Column(String)
    info = Column(String(100))
    email = Column(String(200))
    is_admin = Column(Boolean, default=False)

    def verify_password(self, password):
        if self.password == hashlib.md5(password).hexdigest():
            return True

    def generate_auth_token(self, expiration=6000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'name': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['name'])
        return user
