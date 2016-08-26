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
from sqlalchemy import func

from app.controllers.controller import Base
from app.models.comment import Comment
from app.models.user import User


class Reports(Base):
    def get(self):
        if not current_app.user.is_admin:
            abort(403, 'Forbidden')
        query = User.query.add_columns(func.count()).\
            join(Comment).group_by(User.id)
        count_list = []
        for el in query.all():
            count_list.append({'username': el[0].name, 'count': el[1]})
        return count_list, 200
