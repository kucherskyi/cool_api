from flask import render_template
from flask_script import Command
from flask_mail import Attachment
from datetime import datetime
from sqlalchemy import func, select

from app.const import FORMATS
from app import file_generator
from app import email_sender
from app import amazon_s3 as s3
from app.models.base import db
from app.models.comment import Comment
from app.models.task import Task, UserAndTaskRelation
from app.models.user import User

FORMAT_FUNC = {'json': file_generator.generate_json,
               'csv': file_generator.generate_csv,
               'pdf': file_generator.generate_pdf}


class Commands(Command):

    def run(self, endpoint, email, report_type):
        if endpoint == 'usercomments':
            report_obj = UserComments()
        elif endpoint == 'taskstats':
            report_obj = TaskStats()
        tmpfile = FORMAT_FUNC.get(report_type)(report_obj.get_data(),
                                               template=report_obj.template,
                                               delimiter=report_obj.delimiter,
                                               indent=report_obj.indent,
                                               title=report_obj.title)

        report_name = '{}.{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'),
                                     report_type)

        attachment = Attachment(filename=report_name,
                                content_type=FORMATS.get(report_type),
                                data=tmpfile.read())
        tmpfile.seek(0)
        s3.send_to_s3('reports-json', report_name, tmpfile)
        link = s3.generate_link_to_attach('reports-json', 'Report')
        email_sender.send_mail('Report',
                               render_template('/report_email.html',
                                               user='Admin',
                                               link=link),
                               email,
                               attachment=attachment)
        tmpfile.close()
        print 'Yumm!'


class UserComments():

    title = 'User and Comments report'
    template = '/report.html'
    delimiter = '|'
    indent = 4

    def get_data(self):
        query = User.query.add_columns(func.count())
        query = query.join(Comment).group_by(User.id)
        report_data = []
        for item in query:
            report_data.append({'username': item[0].name, 'count': item[1]})
        return report_data


class TaskStats():

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
