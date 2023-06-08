from flask import Flask
from flask_mysqldb import MySQL

from app import views
from config import Config

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    return app
