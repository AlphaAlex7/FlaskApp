from celery import Celery
from celery.schedules import crontab
from .config import Config_1
from .. import create_app


def make_celery(app=None):
    app = app or create_app()
    celery = Celery(app.name)
    # celery.conf.update(app.config)
    celery.config_from_object(app.config, namespace='CELERY')
    # celery.config_from_object(Config_1, namespace='CELERY')
    TaskBase = celery.Task

    celery.conf.beat_schedule = {
        'post': {
            'task': 'app.celery_app.tasks.post_processor',
            'schedule': crontab(hour="*", minute="*/10"),
            "args": (0, 10)
        },
        'test1': {
            'task': 'app.celery_app.tasks.test',
            'schedule': crontab(hour="*", minute="35"),
        }
    }

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
