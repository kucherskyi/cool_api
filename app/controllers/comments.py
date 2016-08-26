from datetime import datetime
from flask import abort, current_app, g, jsonify, request
from flask.views import MethodView

from app.controllers.controller import auth_token_required


class Comments(MethodView):

    decorators = [auth_token_required]

    def get(self, task_id):
        if not Comments.is_assigned(current_app.user.id, task_id):
            abort(403, 'Forbidden')
        cursor = g.connection.cursor()
        query = 'SELECT user_id, text FROM comments WHERE task_id=%s'
        cursor.execute(query, (task_id, ))
        column_names = [x[0] for x in cursor.description]
        data = []
        for item in cursor.fetchall():
            data.append(dict(zip(column_names, item)))
        return jsonify(data)

    def post(self, task_id):
        if request.mimetype == 'application/json':
            data = request.json
        else:
            data = request.form
        try:
            comment = data['text']
        except KeyError as e:
            return jsonify({'message':
                            {e.message:
                             'Missing required parameter '
                             'in the post body'}}), 400
        if not Comments.is_assigned(current_app.user.id, task_id):
            abort(403, 'Forbidden')
        cursor = g.connection.cursor()
        query = '''INSERT INTO comments
                               (text, user_id, task_id, created_at)
                        VALUES (%s,%s,%s,%s)
                        RETURNING id'''
        post = (comment,
                current_app.user.id,
                task_id,
                datetime.utcnow(),)
        cursor.execute(query, post)
        comment_id = cursor.fetchone()[0]
        g.connection.commit()
        return jsonify({'id': comment_id}), 201

    @staticmethod
    def is_assigned(user_id, task_id):
        cursor = g.connection.cursor()
        query = '''SELECT id FROM user_task_relation
                   WHERE user_id = %s AND task_id = %s'''
        cursor.execute(query, (user_id, task_id,))
        if cursor.rowcount != 1:
            return None
        return g
