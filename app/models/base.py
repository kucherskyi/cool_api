#!env/bin/python

from datetime import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

db = SQLAlchemy()


class Base(db.Model):

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)

