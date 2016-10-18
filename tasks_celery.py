from app.app import celerys

from scripts import Commands


@celerys.task
def create_report(email, report_type):
    command = Commands()
    command.run(email, report_type)
