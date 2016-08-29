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
from xhtml2pdf import pisa

from app.controllers.controller import Base
from app.models.comment import Comment
from app.models.user import User
from app.const import REPORT_FORMATS

parser = reqparse.RequestParser()
parser.add_argument('format', choices=REPORT_FORMATS,
                    location='args',
                    default='json')


class Reports(Base):

    @staticmethod
    def send_mail():
        mail = Mail(current_app)
        msg = Message('Report', sender='testmicoac@gmail.com',
                      recipients=[current_app.user.email])
        msg.body = 'Report'
        with open('/home/artem/tmp.json') as fp:
            msg.attach('/home/artem/tmp.json', 'application/json', fp.read())
        mail.send(msg)

    @staticmethod
    def generate_json(data):
        with open('/home/artem/tmp.json', 'w') as tmp:
            tmp.write(json.dumps(data, sort_keys=True,
                                 indent=4, separators=(',', ': ')))

    @staticmethod
    def generate_csv(data):
        with open('/home/artem/tmp.csv', 'w') as csvtemp:
            headers = data[0].keys()
            writer = csv.DictWriter(csvtemp, fieldnames=headers)
            writer.writeheader()
            for item in data:
                writer.writerow(item)

    @staticmethod
    def generate_pdf(data):
        with open('/home/artem/tmp.pdf', "w+b") as tmp:
            template = render_template('/report_comments.html', items=data)
            pisa.CreatePDF(template, dest=tmp)


class UserComments(Reports):
    def get(self):
        formt = parser.parse_args()
        import pdb; pdb.set_trace()
        if not current_app.user.is_admin:
            abort(403, 'Forbidden')
        query = User.query.add_columns(func.count()).\
            join(Comment).group_by(User.id)
        count_list = []
        for el in query.all():
            count_list.append({'username': el[0].name, 'count': el[1]})
        if formt['format'] == 'json':
            Reports.generate_json(count_list)
        elif formt['format'] == 'csv':
            Reports.generate_csv(count_list)
        elif formt['format'] == 'pdf':
            Reports.generate_pdf(count_list)
        Reports.send_mail()

        return count_list, 200
