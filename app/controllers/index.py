#!env/bin/python

from controller import Base

class Index(Base):
    def get(self):
        return 'Hello'
