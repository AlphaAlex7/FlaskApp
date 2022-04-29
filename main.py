from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import User, Role, ChannelStatistic, ChannelContent, Channel
from app.Init_bd_data import create_test_data

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
def make_init_db():
    """Drop all data in database and Make test Data"""
    db.drop_all()
    db.create_all()
    upgrade()
    create_test_data()


@app.cli.command()
def run():
    app.run()
