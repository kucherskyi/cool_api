from flask import Flask, jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

from models.user import User


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object('config.default')
    app.config.from_envvar('APP_SETTINGS', silent=True)
    app.add_url_rule('/api/login', 'login', _get_token)
    from models.user import db
    db.init_app(app)
    from controllers.index import Index
    from controllers.user import UsersList, UserSingle
    from controllers.tasks import TaskSingle, Tasks, AssignTask
    api.add_resource(Index, '/api/index')
    api.add_resource(UsersList, '/api/users')
    api.add_resource(UserSingle, '/api/users/<user_id>')
    api.add_resource(Tasks, '/api/tasks')
    api.add_resource(TaskSingle, '/api/tasks/<task_id>')
    api.add_resource(AssignTask, '/api/assign_task')
    return app

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(name, password):
    user = User.query.filter_by(name=name).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@auth.login_required
def _get_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401
