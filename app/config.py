import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    SQLALCHEMY_DATABASE_URI = ''.join(
        f"postgresql://postgres"
        f":postgres"
        f"@localhost:5432/flaskapp"
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "strVerySecret"
    # CELERY_BROKER_URL = 'redis://redis:6379/0'
    # CELERY_BROKER = 'redis://redis:6379/0'
    # RESULT_BACKEND = 'redis://redis:6379/0'
    CELERY_BROKER_URL = 'redis://default:redispw@localhost:49153'
    CELERY_BROKER = 'redis://default:redispw@localhost:49154'
    RESULT_BACKEND = 'redis://default:redispw@localhost:49154'
    CELERY_TIMEZONE = 'Europe/Moscow'
    CELERY_IMPORTS = ("app.celery_app.tasks",)


class TestingConfig(LocalConfig):
    TESTING = True
    SERVER_NAME = "127.0.0.0.1:5000"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'test_data.sqlite')}"


class DockerConfig(LocalConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = ''.join(
    #     f"postgresql://postgres"
    #     f":postgres"
    #     f"@flaskpg-13.3:5432/flaskapp"
    # )
    SQLALCHEMY_DATABASE_URI = ''.join(
        f"postgresql://{os.environ.get('POSTGRES_USER')}"
        f":{os.environ.get('POSTGRES_PASSWORD')}"
        f"@db:5432/{os.environ.get('POSTGRES_DB')}"
    )
