#!env/bin/python

from flask import request, current_app
from flask_restful import Resource as BaseResource
from functools import wraps

from app.models.user import User, db


def auth_token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if token is None:
            return {'no token': 'no fun'}, 401
        user = User.verify_auth_token(token)
        if user:
            current_app.user = user
            return fn(*args, **kwargs)
        return 'Invalid token', 401
    return decorated


class Base(BaseResource):
    method_decorators = [auth_token_required]
