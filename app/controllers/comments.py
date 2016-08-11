from datetime import datetime
from flask import current_app, jsonify, abort, request, json
from flask.views import MethodView
import psycopg2

from app.controllers.controller import auth_token_required


class Comments(MethodView):

    decorators = [auth_token_required]

    def get(self, task_id):
        if self.is_assign(task_id):
            connection = psycopg2.connect(self.connect())
            get_comments = connection.cursor()
            query = 'SELECT user_id, text FROM comments WHERE task_id=%s'
            get_variables = (task_id, )
            get_comments.execute(query, get_variables)
            records = get_comments.fetchall()
            column_names = [x[0] for x in get_comments.description]
            data = []
            for item in records:
                data.append(dict(zip(column_names, item)))
            return jsonify(data)
        abort(400)

    def post(self, task_id):
        if self.is_assign(task_id):
            connection = psycopg2.connect(self.connect())
            comment = json.loads(request.data)['comment']
            post_comments = connection.cursor()
            query = '''INSERT INTO comments
                                   (text, user_id, task_id, created_at)
                            VALUES (%s,%s,%s,%s)'''
            post_variables = (comment,
                              current_app.user.id,
                              task_id,
                              datetime.utcnow(),)
            post_comments.execute(query, post_variables)
            connection.commit()
            post_comments.close()
            return jsonify({'comment': comment}), 201

    @staticmethod
    def connect():
        db_name = current_app.config[
            'SQLALCHEMY_DATABASE_URI'].split('/')[-1:][0]
        db_host = 'localhost'
        db_user = 'admin'
        db_pass = 'pass'
        conn_string = "host={} dbname={} user={} password={}".format(
            db_host, db_name, db_user, db_pass)
        return conn_string

    @staticmethod
    def is_assign(task_id):
        is_assigned = Comments.connect()
        connection = psycopg2.connect(is_assigned)
        check = connection.cursor()
        query = '''SELECT * FROM user_task_relation
                           WHERE user_id = %s AND task_id = %s'''
        condition = (current_app.user.id, task_id,)
        check.execute(query, condition)
        if check.fetchall() == []:
            return False
        return True
