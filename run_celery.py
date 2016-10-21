from app.app import create_app
from tasks_celery import celery

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        celery.start()