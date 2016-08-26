from flask import g, current_app, request
import psycopg2
from urlparse import urlparse

from endpoints import COMMENTS

_CONNECTION_STRING = ''


def establish_connection(app):
    if not _CONNECTION_STRING:
        global _CONNECTION_STRING
        db_uri = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
        _CONNECTION_STRING = "host={} dbname={} user={} password={}".format(
            db_uri.hostname, db_uri.path[1:], db_uri.username, db_uri.password)
    connection = psycopg2.connect(_CONNECTION_STRING)
    return connection


def before_request():
    if request.endpoint == COMMENTS:
        g.connection = establish_connection(current_app)


def after_request(response=None):
    if hasattr(g, 'connection'):
        g.connection.close()
    return response
