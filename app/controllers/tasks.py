from flask import abort, current_app
from flask_restful import marshal_with, reqparse, fields
from sqlalchemy.exc import DataError, IntegrityError

from app.controllers.controller import Base
from app.models.task import Task, db, UserAndTaskRelation

RETURN_TASK = {
    'id': fields.Integer,
    'title': fields.String,
    'status': fields.String,
    'users': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
}

RETURN_TASK_LIST = {
    'id': fields.Integer,
    'title': fields.String,
    'status': fields.String,
    'users': fields.String,
}


post_task = reqparse.RequestParser()
post_task.add_argument('title', type=str, required=True)
post_task.add_argument('status', choices=['completed', 'in_progress'],
                       required=True)

put_task = reqparse.RequestParser()
put_task.add_argument(
    'status', choices=['completed', 'in_progress'], required=True)

assign_task = reqparse.RequestParser()
assign_task.add_argument('user_id', type=int, required=True)
assign_task.add_argument('task_id', type=int, required=True)


class Tasks(Base):

    @marshal_with(RETURN_TASK_LIST)
    def get(self):
        tasks = Task.query.join(UserAndTaskRelation).filter(
            UserAndTaskRelation.user_id == current_app.user.id)
        return tasks.all()

    @marshal_with(RETURN_TASK_LIST)
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
    @marshal_with(RETURN_TASK)
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.is_assigned(task_id, current_app.user.id):
            return task
        abort(403, 'Forbidden')

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.is_assigned(task_id, current_app.user.id):
            db.session.delete(task)
            db.session.commit()
            return '', 204
        abort(403, 'Forbidden')

    @marshal_with(RETURN_TASK)
    def put(self, task_id):
        args = put_task.parse_args()
        task = Task.query.get_or_404(task_id)
        if task.is_assigned(task_id, current_app.user.id):
            task.status = args['status']
            try:
                db.session.commit()
                return task, 200
            except DataError as e:
                db.session.rollback()
                abort(400, str(e))
        abort(403, 'Forbidden')


class AssignTask(Base):

    @marshal_with(RETURN_TASK)
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
