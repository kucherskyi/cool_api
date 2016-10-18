from flask_script import Command


class Commands(Command):
    def run(self, email, report_type):
        print email, report_type
