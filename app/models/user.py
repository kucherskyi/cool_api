#!env/bin/python

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import hashlib
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


db = SQLAlchemy()


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())


class User(Base):
    __tablename__ = 'users'
    name = db.Column(db.String(32))
    password = db.Column(db.String)
    info = db.Column(db.String(100))
    is_admin = db.Column(db.Integer, default=1)

    def verify_password(self, password):
        if self.password == hashlib.md5(password).hexdigest():
            return True

    def generate_auth_token(self, expiration=600):
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
