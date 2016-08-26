# -*- coding: utf-8 -*-

from flask import abort
from flask_restful import marshal_with, reqparse, inputs, fields
import hashlib
from sqlalchemy.exc import DataError, IntegrityError
import re

from app.controllers.controller import Base
from app.models.user import User
from app.models.base import db


RETURN_USER = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'info': fields.String,
    'is_admin': fields.Boolean,
    'tasks': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
}

RETURN_USERS_LIST = {
    'id': fields.Integer,
    'name': fields.String
}

RETURN_USER_ID = {
    'id': fields.Integer
}

RETURN_PUT_USER = {
    'id': fields.Integer,
    'info': fields.String
}


def email(address):
    regex = "^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    if re.match(regex, address):
        return address
    else:
        raise ValueError('{} is not a valid email'.format(address))


post_user = reqparse.RequestParser()
post_user.add_argument('name', type=str, required=True)
post_user.add_argument('password', type=str, required=True)
post_user.add_argument('info', type=str)
post_user.add_argument('email', type=email, required=True)
post_user.add_argument('is_admin', type=inputs.boolean)


put_user = reqparse.RequestParser()
put_user.add_argument('info', type=str, required=True)


class UsersList(Base):
    @marshal_with(RETURN_USERS_LIST)
    def get(self):
        return User.query.all()

    @marshal_with(RETURN_USER_ID)
    def post(self):
        args = post_user.parse_args()
        user = User(**args)
        user.password = hashlib.md5(args['password']).hexdigest()
        try:
            db.session.add(user)
            db.session.commit()
        except (DataError, IntegrityError) as e:
            db.session.rollback()
            abort(400, str(e))
        return user, 201


class UserSingle(Base):
    @marshal_with(RETURN_USER)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @marshal_with(RETURN_PUT_USER)
    def put(self, user_id):
        args = put_user.parse_args()
        user = User.query.get_or_404(user_id)
        user.info =  args['info']
        try:
            db.session.commit()
            return user, 200
        except DataError as e:
            abort(400, str(e))
