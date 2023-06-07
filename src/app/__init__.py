from flask import Flask

from app import views
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

if __name__ == '__main__':
    app.run()
