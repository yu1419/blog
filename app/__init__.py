from flask import Flask
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import os
from flask import Flask, render_template, session
from flask import redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from .database.connect_db import get_db

login_manager = LoginManager()

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

    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    expiration = 3600

    app.config['SECRET_KEY'] = 'hard to guess string'


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
