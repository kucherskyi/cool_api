from flask import abort
from flask_restful import marshal_with, reqparse, inputs
import hashlib
from sqlalchemy.exc import DataError, IntegrityError

from app.controllers.controller import Base
from app.controllers.marshalling_fields import *
from app.models.user import User, db

post_user = reqparse.RequestParser()
post_user.add_argument('name', type=str, required=True)
post_user.add_argument('password', type=str, required=True)
post_user.add_argument('info', type=str)
post_user.add_argument('email', type=str, required=True)
post_user.add_argument('is_admin', type=inputs.boolean)


put_user = reqparse.RequestParser()
put_user.add_argument('info', type=str, required=True)


class UsersList(Base):
    @marshal_with(RESPONSE_USER_LIST)
    def get(self):
        return User.query.all()

    @marshal_with(RETURN_USER)
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
    @marshal_with(RESPONSE_USER)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @marshal_with(RETURN_PUT)
    def put(self, user_id):
        args = put_user.parse_args()
        user = User.query.get_or_404(user_id)
        user.info = args['info']
        try:
            db.session.commit()
            return user, 200
        except DataError as e:
            abort(400, str(e))
