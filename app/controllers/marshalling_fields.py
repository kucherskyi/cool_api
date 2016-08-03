from flask_restful import fields

RESPONSE_USER = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'info': fields.String,
    'is_admin': fields.Boolean,
    'tasks':fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
}

RESPONSE_USER_LIST = {
    'id': fields.Integer,
    'name': fields.String
}

RETURN_USER = {
    'id': fields.Integer
}

RETURN_PUT = {
    'id': fields.Integer,
    'info': fields.String
}

RESPONSE_TASK = {
    'id': fields.Integer,
    'title': fields.String,
    'status': fields.String,
    'users': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
}

TASK = {
    'id': fields.Integer,
    'title': fields.String,
    'status': fields.String,
    'users': fields.String,
}
