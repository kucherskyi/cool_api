from flask import abort, current_app
from flask_restful import marshal_with, reqparse
from sqlalchemy.exc import DataError, IntegrityError
import re

from app.controllers.controller import Base
from app.controllers.marshalling_fields import *
from app.models.user import Task, db, UserAndTaskRelation


post_task = reqparse.RequestParser()
post_task.add_argument('title', type=str, required=True)
post_task.add_argument('status', type=str, required=True)

put_task = reqparse.RequestParser()
put_task.add_argument('status', type=str, required=True)

assign_task = reqparse.RequestParser()
assign_task.add_argument('user_id', type=int, required=True)
assign_task.add_argument('task_id', type=int, required=True)


class Tasks(Base):

    @marshal_with(TASK)
    def get(self):
        tasks = Task.query.join(UserAndTaskRelation).filter(
            UserAndTaskRelation.user_id == current_app.user.id)
        return tasks.all()

    @marshal_with(TASK)
    def post(self):
        args = post_task.parse_args()
        task = Task(**args)
        task.assign_user(current_app.user.id)
        try:
            db.session.add(task)
            db.session.commit()
        except DataError as e:
            db.session.rollback()
            abort(400, str(e))
        return task, 201


class TaskSingle(Base):
    @marshal_with(RESPONSE_TASK)
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        for user in task.users:
            if user.id == current_app.user.id:
                return task
        return abort(403, 'Forbidden')

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        for user in task.users:
            if user.id == current_app.user.id:
                db.session.delete(task)
                db.session.commit()
                return '', 204
        return abort(403, 'Forbidden')

    @marshal_with(RESPONSE_TASK)
    def put(self, task_id):
        args = put_task.parse_args()
        task = Task.query.get_or_404(task_id)
        for user in task.users:
            if user.id == current_app.user.id:
                task.status = args['status']
                try:
                    db.session.commit()
                    return task, 200
                except DataError as e:
                    db.session.rollback()
                    abort(400, str(e))
        return abort(403, 'Forbidden')


class AssignTask(Base):

    @marshal_with(RESPONSE_TASK)
    def post(self):
        args = assign_task.parse_args()
        task = Task.query.get_or_404(args['task_id'])
        task.assign_user(args['user_id'])
        try:
            db.session.add(task)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, str(e))
        return task, 201
