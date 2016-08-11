from flask import current_app
import hashlib
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.comment import Comment
from app.models.task import UserAndTaskRelation


class User(Base):

    __tablename__ = 'users'
    name = Column(String(200), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    info = Column(Text)
    email = Column(String(254), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    comments = relationship('Comment', backref='users')
    tasks = relationship('Task', secondary='user_task_relation', viewonly=True)

    def assign_task(self, task_id):
        self.user_task_relation.append(UserAndTaskRelation(user_id=self.id,
                                                           task_id=task_id))

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
