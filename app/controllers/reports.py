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

import csv
from flask import current_app, abort, render_template
from flask_restful import reqparse
from flask_mail import Mail, Message
import json
from sqlalchemy import func
import tempfile
from xhtml2pdf import pisa

from app.controllers.controller import Base
from app.const import FORMATS
from app.models.comment import Comment
from app.models.user import User

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

    @staticmethod
    def send_mail(data, formt):
        temp = tempfile.TemporaryFile()
        if formt == 'json':
            temp.write(json.dumps(data,
                                  sort_keys=True,
                                  indent=4,
                                  separators=(',', ': ')))

        elif formt == 'csv':
            headers = data[0].keys()
            writer = csv.DictWriter(temp, fieldnames=headers)
            writer.writeheader()
            for item in data:
                writer.writerow(item)

        elif formt == 'pdf':
            template = render_template('/report_comments.html', items=data)
            pisa.CreatePDF(template, dest=temp)

        temp.seek(0)
        mail = Mail(current_app)
        msg = Message('Report', sender='testmicoac@gmail.com',
                      recipients=[current_app.user.email])
        msg.body = 'Report'
        msg.attach('Report', FORMATS.get(formt), temp.read())
        mail.send(msg)
        temp.close()


class UserComments(Reports):

    def get(self):
        formt = parser.parse_args()
        query = User.query.add_columns(func.count())
        query = query.join(Comment).group_by(User.id)
        count_list = []
        for el in query.all():
            count_list.append({'username': el[0].name, 'count': el[1]})
        self.send_mail(count_list, formt['format'])
        return {'status': 'sent'}, 200
