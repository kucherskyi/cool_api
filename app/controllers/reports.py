from datetime import datetime
from flask_mail import Attachment
from flask import current_app, abort
from flask_restful import reqparse
from sqlalchemy import func, select
import os

from tasks_celery import create_report
from app.controllers.controller import Base
from app.const import FORMATS
from app import amazon_s3 as s3
from app import email_sender
from app import file_generator
from app.models.user import User
from app.models.base import db
from app.models.comment import Comment
from app.models.task import Task, UserAndTaskRelation

parser = reqparse.RequestParser()
parser.add_argument('format', choices=FORMATS.keys(),
                    location='args',
                    default='json')

FORMAT_FUNC = {'json': file_generator.generate_json,
               'csv': file_generator.generate_csv,
               'pdf': file_generator.generate_pdf}


def admin_required(fn):
    def decorated(*args, **kwargs):
        if current_app.user.is_admin:
            return fn(*args, **kwargs)
        abort(403, 'Forbidden')
    return decorated


class Reports(Base):

    def get(self):
        arg = parser.parse_args()
        create_report.apply_async(args=[current_app.user.email,
                                        arg.format])
        return {'status': 'processing'}

    def _get_task(self):
        raise NotImplementedError


class UserComments(Reports):

    title = 'Task stats report'
    template = '/report.html'
    delimiter = ','
    indent = 4

    def get_data(self):
        query = User.query.add_columns(func.count())
        query = query.join(Comment).group_by(User.id)
        report_data = []
        for item in query:
            report_data.append({'username': item[0].name, 'count': item[1]})
        return report_data

    def _get_task(self, subject, body, recipients):
        script = 'python /home/artem/cool_api_git/cool_api/scripts.py \
        send_email {} "{}" {}'.format(subject, str(body), recipients)
        os.system(script)


class TaskStats(Reports):

    title = 'Task stats report'
    template = '/report.html'
    delimiter = ','
    indent = 4

    def get_data(self):
        users_count = select([func.count()]).where(
            UserAndTaskRelation.task_id == Task.id).label('users')
        comments_count = select([func.count()]).where(
            Comment.task_id == Task.id).label('comments')
        query = db.session.query(Task.id, Task.title,
                                 users_count, comments_count)
        report_data = []
        for item in query:
            report_data.append(item._asdict())
        return report_data

    def _get_task(self, subject, body, recipients, attachment):
        email_sender.send_mail(subject, body, recipients,
                               attachment=attachment)

# class Reports(Base):

#     method_decorators = [admin_required] + Base.method_decorators[:]

#     def get(self):
#         args = parser.parse_args()
#         tmpfile = FORMAT_FUNC.get(args['format'])(self.get_data(),
#                                                   template=self.template,
#                                                   delimiter=self.delimiter,
#                                                   indent=self.indent,
#                                                   title=self.title)
#         file_name = '{}_{}.{}'.format(current_app.user.name,
#                                       datetime.now().strftime('%Y%m%d%H%M%S'),
#                                       args['format'])
#         attachment = Attachment(filename=file_name,
#                                 content_type=FORMATS.get(args['format']),
#                                 data=tmpfile.read())
#         tmpfile.seek(0)
#         s3.send_to_s3('reports-json', file_name, tmpfile)
#         link = s3.generate_link_to_attach('reports-json', file_name)
#         import pdb; pdb.set_trace()
#         send_data(json.dumps({'subject': 'Report',
#                    'html': render_template('report_email.html',
#                                            user=current_app.user.name,
#                                            link=link),
#                    'recipients': current_app.user.email,
#                    'attachment': pickle.dumps(attachment)}))
#         tmpfile.close()
#         return {'status': 'sent'}

#     def get_data():
#         raise NotImplementedError


# class UserComments(Reports):

#     title = 'User and Comments report'
#     template = '/report.html'
#     delimiter = '|'
#     indent = 4

#     def get_data(self):
#         query = User.query.add_columns(func.count())
#         query = query.join(Comment).group_by(User.id)
#         report_data = []
#         for item in query:
#             report_data.append({'username': item[0].name, 'count': item[1]})
#         return report_data


# class TaskStats(Reports):

#     title = 'Task stats report'
#     template = '/report.html'
#     delimiter = ','
#     indent = 4

#     def get_data(self):
#         users_count = select([func.count()]).where(
#             UserAndTaskRelation.task_id == Task.id).label('users')
#         comments_count = select([func.count()]).where(
#             Comment.task_id == Task.id).label('comments')
#         query = db.session.query(Task.id, Task.title,
#                                  users_count, comments_count)
#         report_data = []
#         for item in query:
#             report_data.append(item._asdict())
#         return report_data
