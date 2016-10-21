from flask import current_app, abort
from flask_restful import reqparse

from tasks_celery import create_report
from app.controllers.controller import Base
from app.const import FORMATS


parser = reqparse.RequestParser()
parser.add_argument('format', choices=FORMATS.keys(),
                    location='args',
                    default='json')


def admin_required(fn):
    def decorated(*args, **kwargs):
        if current_app.user.is_admin:
            return fn(*args, **kwargs)
        abort(403, 'Forbidden')
    return decorated


class Reports(Base):

    method_decorators = [admin_required] + Base.method_decorators[:]

    def get(self):
        arg = parser.parse_args()
        create_report.apply_async(args=[self.endpoint,
                                  current_app.user.email,
                                        arg.format])
        return {'status': 'processing'}


class UserComments(Reports):
    pass


class TaskStats(Reports):
    pass
