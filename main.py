from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import User, Role, ChannelStatistic, \
    ChannelContent, Channel, ScheduleContent,\
    ScheduleRegular, ScheduleRegularType
from app.init_db_data import create_test_data
from app.celery_app import make_celery

app = create_app()
migrate = Migrate(app, db)
celery = make_celery(app)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Role=Role,
        ChannelStatistic=ChannelStatistic,
        ChannelContent=ChannelContent,
        Channel=Channel
    )


@app.cli.command()
def make_init_db():
    """Drop all data in database and Make test Data"""
    db.drop_all()
    db.create_all()
    upgrade()
    create_test_data()


@app.cli.command()
def run():
    app.run()
