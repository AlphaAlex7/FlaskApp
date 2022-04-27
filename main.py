from flask_migrate import Migrate, upgrade
import click

from app import create_app, db
from app.models import User, Role, ChannelStatistic, ChannelContent, Channel
from app.Init_bd_data import create_user, create_channel, create_channel_stat

app = create_app()
migrate = Migrate(app, db)


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
def make_db():
    """Run deployment tasks."""
    Role.insert_roles()
    # create_user()

    # create_channel()
    create_channel_stat()


@app.cli.command()
def db_test_data():
    """Run test_data"""
    db.drop_all()
    db.create_all()
    upgrade()

    Role.insert_roles()
    create_user()

    create_channel()
    create_channel_stat()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()

    Role.insert_roles()


@app.cli.command()
def run():
    app.run()
