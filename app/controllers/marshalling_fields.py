#!env/bin/python

from flask_restful import fields

RESPONSE_USER = {
    'id': fields.Integer,
    'name': fields.Raw,
    'email': fields.Raw,
    'info': fields.Raw,
    'is_admin': fields.Boolean,
    'created_at': fields.String,
    'updated_at': fields.String
}

RESPONSE_USER_LIST = {
    'id': fields.Integer,
    'name': fields.Raw
}

RETURN_USER = {
    'id': fields.Integer
}

RETURN_PUT = {
    'id': fields.Integer,
    'info': fields.Raw
}
