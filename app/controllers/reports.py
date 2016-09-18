from datetime import datetime
from flask_mail import Attachment
from flask import current_app, abort, render_template
from flask_restful import reqparse
from sqlalchemy import func, select


from app.controllers.controller import Base
from app.const import FORMATS
from app import file_generator
from app import email_sender
from app import amazon_s3 as s3
from app.models.comment import Comment
from app.models.user import User
from app.models.base import db
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

    method_decorators = [admin_required] + Base.method_decorators[:]

    def get(self):
        args = parser.parse_args()
        tmpfile = FORMAT_FUNC.get(args['format'])(self.get_data(),
                                                  template=self.template,
                                                  delimiter=self.delimiter,
                                                  indent=self.indent)

        file_name = '{}_{}.{}'.format(current_app.user.name,
                                      datetime.now().strftime('%Y%m%d%H%M%S'),
                                      args['format'])
        attachment = Attachment(filename=file_name,
                                content_type=FORMATS.get(args['format']),
                                data=tmpfile.read())
        s3.send_to_s3('flask-reports', file_name, tmpfile)
        link = s3.generate_link_to_attach('flask-reports', file_name)
        email_sender.send_mail('Report',
                               render_template('report_email.html',
                                               user=current_app.user.name,
                                               link=link),
                               current_app.user.email,
                               attachment=attachment)
        tmpfile.close()
        return {'status': 'sent'}

    def get_data():
        raise NotImplementedError


class UserComments(Reports):

    template = '/report_comments.html'
    delimiter = '|'
    indent = 4

    def get_data(self):
        query = User.query.add_columns(func.count())
        query = query.join(Comment).group_by(User.id)
        report_data = []
        for item in query:
            report_data.append({'username': item[0].name, 'count': item[1]})
        return report_data


class TaskStats(Reports):

    template = '/report_tasks.html'
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
