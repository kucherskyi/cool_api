from flask_restful import reqparse

post_user = reqparse.RequestParser()
post_user.add_argument('name', type=str, required=True)
post_user.add_argument('password', type=str, required=True)
post_user.add_argument('info', type=str, required=False)
post_user.add_argument('email', type=str, required=True)
post_user.add_argument('is_admin')


put_user = reqparse.RequestParser()
put_user.add_argument('info', type=str, required=False)
