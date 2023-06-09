from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL

from app.urls import add_routes
from config import Config
from app.models import User

mysql = MySQL()
login_manager = LoginManager()

login_manager.login_view = 'signin'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    app.extensions['mysql'] = mysql
    login_manager.init_app(app)
    app.extensions['flask_login'] = login_manager

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user(user_id)
    add_routes(app)
    return app
