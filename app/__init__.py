import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

bootstrap = Bootstrap5()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = None
login_manager.login_view = 'auth.login'


def create_app():
    main_app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))

    main_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    main_app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    main_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    main_app.config['SECRET_KEY'] = "0x469f4bc784e6d845"  # flask_password
    bootstrap.init_app(main_app)
    db.init_app(main_app)
    login_manager.init_app(main_app)

    from .api import api
    main_app.register_blueprint(api, url_prefix="/api/")

    from .statistic import statistic
    main_app.register_blueprint(statistic)

    from .auth import auth
    main_app.register_blueprint(auth, url_prefix="/auth/")

    return main_app
