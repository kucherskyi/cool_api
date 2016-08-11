from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import UniqueConstraint, Enum
from sqlalchemy.orm import relationship, backref

from app.const import TASK_STATUSES
from app.models.base import Base, db
from app.models.comment import Comment


class UserAndTaskRelation(Base):

    __tablename__ = 'user_task_relation'
    __table_args__ = (UniqueConstraint('user_id', 'task_id'),)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)

    user_relation = relationship('User',
                                 backref=backref('user_task_relation',
                                                 cascade="all, delete-orphan"))
    task_relation = relationship('Task',
                                 backref=backref('user_task_relation',
                                                 cascade="all, delete-orphan"))


class Task(Base):

    __tablename__ = 'tasks'

    title = Column(String(200), nullable=False)
    status = Column(Enum(*TASK_STATUSES, name='statuses'),
                    nullable=False)

    comments = relationship('Comment', backref='tasks')
    users = relationship('User', secondary='user_task_relation', viewonly=True)

    def assign_user(self, user_id):
        self.user_task_relation.append(UserAndTaskRelation(user_id=user_id,
                                                           task_id=self.id))

    @staticmethod
    def is_assigned(task_id, user_id):
        is_assigned = db.session.query(UserAndTaskRelation).filter(
            UserAndTaskRelation.user_id == user_id).filter(
            UserAndTaskRelation.task_id == task_id)
        return is_assigned.count() == 1


