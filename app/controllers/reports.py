'''
User stories:
1. Project admins want to receive reports for future analysing.
2. There are 2 types of reports:
    - users comments: user name and total number of comments.
    - task average usage: should return all tasks with quantities of
    assigned users and comments, and deltas(user count and comments count)
    between average values (for all tasks) and values for current task
    (in percents).
3. User could select format for report. Supported formats cvs, json and pdf.
4. Generated report should be sent to admin email.
On phase one it is ok to generate report in web application but our
next improvement will be moving reports generation to another server.
Please think about solution and investigate libraries you will use.
'''

from flask import current_app, abort
from flask_restful import reqparse
from sqlalchemy import func


from app.controllers.controller import Base
from app.const import FORMATS
from app.file_generator import *
from app.email_sender import *
from app.models.comment import Comment
from app.models.user import User


FORMAT_FUNC = {'json': generate_json,
               'csv': generate_csv,
               'pdf': generate_pdf}

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
        args = parser.parse_args()
        data = self.get_data()
        file = FORMAT_FUNC.get(args['format'])(data, template=self.template,
                                               delimiter=self.delimiter,
                                               indent=self.indent)
        try:
            send_mail(current_app, file, FORMATS.get(args['format']))
        except Exception as e:
            abort(400, str(e))
        file.close()
        return {'status': 'sent'}, 200

    def get_data():
        pass


class UserComments(Reports):

    template = '/report_comments.html'
    delimiter = '|'
    indent = 4

    def get_data(self):
        query = User.query.add_columns(func.count())
        query = query.join(Comment).group_by(User.id)
        count_list = []
        for el in query.all():
            count_list.append({'username': el[0].name, 'count': el[1]})
        return count_list


a = Reports()


class B(Reports):
    pass
