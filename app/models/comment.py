from sqlalchemy import Column, Text, ForeignKey, Integer

from app.models.base import Base


class Comment(Base):

    __tablename__ = 'comments'
    text = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '{}'.format(self.text)
