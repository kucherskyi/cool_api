from flask_script import Manager

from app import email_sender
from app.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def send_email(subject, body, recipient):
    email_sender.send_mail(subject, body, recipient)


if __name__ == '__main__':
    manager.run()
