from flask import current_app, abort
from flask_restful import reqparse
from sqlalchemy import func, select


from app.controllers.controller import Base
from app.const import FORMATS
from app import file_generator
from app import email_sender
from app.models.comment import Comment
from app.models.user import User
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

        try:
            email_sender.send_mail(current_app, tmpfile,
                                   FORMATS.get(args['format']))
        except AttributeError as e:
            abort(400, str(e))
        finally:
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
        query = Task.query.add_columns(Task.title, users_count, comments_count)
        report_data = []
        for item in query:
            tmp = {}
            for k in item.keys():
                try:
                    tmp[k] = getattr(item, k).id
                except AttributeError:
                    tmp[k] = getattr(item, k)
            report_data.append(tmp)
        return report_data
