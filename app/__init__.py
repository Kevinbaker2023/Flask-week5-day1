from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
db = SQLAlchemy()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

login_manager.login_view = 'login'
login_manager.login_message = 'Please sign up or login to access this page'
login_manager.login_message_category = 'info'


from app import routes, models