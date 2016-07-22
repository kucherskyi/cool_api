#!env/bin/python

from flask import jsonify, abort
from flask_restful import reqparse, fields, marshal_with
from psycopg2 import IntegrityError

from app.models.user import User, db
from controller import Base
import hashlib

responce_user = {
    'id': fields.Integer,
    'name': fields.Raw,
    'email': fields.Raw,
    'info': fields.Raw,
    'is_admin': fields.Boolean,
    'created_at':fields.String,
    'updated_at':fields.String
}

responce_user_list = {
    'id': fields.Integer,
    'name': fields.Raw
}


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('info')
parser.add_argument('email')
parser.add_argument('is_admin')


class UsersList(Base):
    @marshal_with(responce_user_list)
    def get(self):
        all_users = []
        for row in db.session.query(User).all():
            all_users.append(row)
        return all_users

    def post(self):
        args = parser.parse_args()
        name = args['name']
        password = hashlib.md5(args['password']).hexdigest()
        email = args['email']
        info = args['info']
        is_admin = args['is_admin']
        try:
            user = User(name=name,
                        info=info,
                        password=password,
                        email=email,
                        is_admin = is_admin)
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            print e
        return args['name'], 201


class UserSingle(Base):
    @marshal_with(responce_user)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(400, error_message='No user with id={}'.format(user_id))
        return user

    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return 'deleted', 204

    def put(self, user_id):
        args = parser.parse_args()
        user = User.query.get(user_id)
        user.info = args['info']
        db.session.add(user)
        db.session.commit()
        return jsonify({'name': user.info})
