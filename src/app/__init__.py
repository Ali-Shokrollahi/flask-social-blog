from flask import Flask
from flask_mysqldb import MySQL

from app.urls import add_routes
from config import Config

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    app.extensions['mysql'] = mysql
    add_routes(app)
    return app
