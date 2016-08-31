from flask_mail import Mail, Message


def send_mail(app, data, format,
              mail_title='Report',
              file_name='Report',
              sender='testmicoac@gmail.com'):

    mail = Mail(app)
    msg = Message(mail_title, sender=sender,
                  recipients=[app.user.email])
    msg.body = mail_title
    msg.attach(file_name, format, data.read())
    try:
        mail.send(msg)
    except Exception:
        return False
    return True
