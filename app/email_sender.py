from flask import current_app
import flask_mail


mail = None


def send_mail(subject, html, recipients, attachment=None):
    if not mail:
        global mail
        mail = flask_mail.Mail(current_app)
    message = flask_mail.Message(subject,
                                 recipients=[recipients],
                                 html=html)

    if attachment:
        message.attach(attachment.filename,
                       attachment.content_type,
                       attachment.data)

    mail.send(message)
