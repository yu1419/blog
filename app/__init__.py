from flask import Flask
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import os
from flask import Flask, render_template, session
from flask import redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from .database.connect_db import get_db
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
import markdown
from flask import Markup
from .database import db
from .helper import *
from .models import AnonymousUser
from flask_mail import Mail, Message


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


pagedown = PageDown()
mail = Mail()

def id_to_username(user_id):
    sql = "select user_name from user where user_id = %s"
    with db.cursor() as cursor:
        cursor.execute(sql, (user_id, ))
        return cursor.fetchone()


def create_app():
    app = Flask(__name__)


    expiration = 3600
    Markdown(app)
    login_manager.anonymous_user = AnonymousUser

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['SECRET_KEY'] = 'hard to guess string'
    app.jinja_env.globals['id_to_username'] = id_to_username
    app.jinja_env.globals['markdown'] = markdown
    app.jinja_env.globals['Markup'] = Markup

    mail.init_app(app)
    pagedown.init_app(app)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .member import member as member_blueprint
    app.register_blueprint(member_blueprint, url_prefix='/member')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
