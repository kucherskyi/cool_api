import os
TESTING = False
CSRF_ENABLED = True
DEBUG = True
SECRET_KEY = 'sk'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'testmicoac@gmail.com'
MAIL_PASSWORD = '123zxc12'
MAIL_DEFAULT_SENDER = 'testmicoac@gmail.com'
