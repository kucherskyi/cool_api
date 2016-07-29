from flask import current_app
import hashlib
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship, backref

from app.models.base import Base, db


class UserAndTaskRelation(Base):

    __tablename__ = 'user_task_relation'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)

    user_relation = relationship('User',
                                 backref=backref('user_task_relation',
                                                 cascade="all, delete-orphan"))
    task_relation = relationship('Task',
                                 backref=backref('user_task_relation',
                                                 cascade="all, delete-orphan"))

    __table_args__ = (UniqueConstraint('user_id', 'task_id'),)


class User(Base):

    __tablename__ = 'users'
    name = Column(String(200), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    info = Column(Text)
    email = Column(String(254), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    tasks = relationship('Task', secondary='user_task_relation')

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


class Task(Base):

    __tablename__ = 'tasks'

    title = Column(String(200), nullable=False)
    status = Column(String(15), nullable=False)

    users = relationship('User', secondary='user_task_relation')

    def assign_user(self, user_id):
        self.user_task_relation.append(UserAndTaskRelation(user_id=user_id,
                                                           task_id=self.id))
