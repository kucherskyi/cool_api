from celery import Celery
from flask import current_app
from scripts import Commands

from config import celery_config


celery = Celery()
celery.config_from_object(celery_config)


@celery.task
def create_report(endpoint, email, report_type):
    command = Commands()
    with current_app.app_context():
        command.run(endpoint, email, report_type)
