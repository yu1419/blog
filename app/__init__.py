from flask import Flask
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import os
from flask import Flask, render_template, session
from flask import redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from .database.connect_db import get_db

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
SSL_DISABLE = False
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
FLASKY_POSTS_PER_PAGE = 20
FLASKY_FOLLOWERS_PER_PAGE = 50
FLASKY_COMMENTS_PER_PAGE = 30
FLASKY_SLOW_DB_QUERY_TIME=0.5

db = get_db()

def create_app():
    app = Flask(__name__)


    login_manager = LoginManager()
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    expiration = 3600


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
