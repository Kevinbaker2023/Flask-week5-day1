from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_factory():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign up or login to access this page'
    login_manager.login_message_category = 'info'

    from app.blueprints.auth import auth
    from app.blueprints.pokemon import pokemon

    app.register_blueprint(auth)
    app.register_blueprint(pokemon)

    return app

from app import models