from celery import Celery

from .. import create_app


def make_celery(app=None):
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    celery.conf.beat_schedule = {
        'new post': {
            'task': 'app.celery_app.tasks.task_1',
            'schedule': 10.0,
        }
    }

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
