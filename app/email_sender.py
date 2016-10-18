import flask_mail
from flask import current_app


mail = None

def send_mail(subject, body, recipients, attachment=None):

    with current_app.app_context():
        if not mail:
            global mail
            mail = flask_mail.Mail(current_app)
            message = flask_mail.Message(subject=subject,
                                         recipients=[recipients],
                                         body=body)
            if attachment:
                message.attach(attachment.filename,
                               attachment.content_type,
                               attachment.data)
            mail.send(message)
