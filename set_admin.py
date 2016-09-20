from argparse import ArgumentParser
from flask_script import Manager, Command
from sqlalchemy.orm.exc import NoResultFound

from app.app import create_app
from app.models.user import User
from app.models.base import db


manager = Manager(create_app())
parser = ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()


class AdminSetter(Command):

    def run(self):
        try:
            user = db.session.query(User).filter_by(name=args.name).one()
            user.is_admin = True
            db.session.commit()
            print 'Done! {} is admin now!'.format(args.name)
        except NoResultFound, e:
            print e


manager.add_command(args.name, AdminSetter())

if __name__ == "__main__":
    manager.run()
