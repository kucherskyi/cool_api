#!env/bin/python

from app.controllers.controller import Base

class Index(Base):
    def get(self):
        return 'Hello'
