from flask import request, current_app, abort
from flask_restful import Resource as BaseResource
from flask_restful import reqparse, marshal
from sqlalchemy.exc import DataError
from functools import wraps

from app.models.user import User

parser = reqparse.RequestParser()
parser.add_argument('offset', type=int, location='args', default=0)
parser.add_argument('limit', type=int, location='args', default=20)


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


def pagination(pagination_fields):
    def decorate(fn):
        def wrapper(*args, **kwargs):
            paginate = parser.parse_args()
            query = fn(*args, **kwargs)
            if paginate['offset'] >= query.count():
                paginate['offset'] = query.count() - 1
            try:
                result = query.offset(
                    paginate['offset']).limit(paginate['limit'])
                return {'user': current_app.user.id,
                        'total': query.count(),
                        'tasks': marshal(result.all(), pagination_fields),
                        'offset': paginate['offset'],
                        'limit': paginate['limit']}
            except DataError as e:
                abort(400, str(e))
        return wrapper
    return decorate


class Base(BaseResource):
    method_decorators = [auth_token_required]
