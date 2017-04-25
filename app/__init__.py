from flask import Flask
from flask_login import LoginManager
import os
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
import markdown
from flask import Markup
from .database import db, get_db
from .helper import *
from .models import AnonymousUser
from flask_mail import Mail
from .fake_data import fake_data

login_manager = LoginManager()
pagedown = PageDown()
mail = Mail()
bootstrap = Bootstrap()


def id_to_username(user_id):
    # add to jinji environment
    # convert user_id to user name
    sql = "select user_name from user where user_id = %s"
    user_name = None
    with db.cursor() as cursor:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        if result:
            user_name = result["user_name"]
    return user_name


def create_app(add_fake=False):
    app = Flask(__name__)
    Markdown(app)
    login_manager.anonymous_user = AnonymousUser

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['SECRET_KEY'] = 'hard to guess string'

    app.jinja_env.globals['markdown'] = markdown
    app.jinja_env.globals['Markup'] = Markup

    app.jinja_env.globals['id_to_username'] = id_to_username

    bootstrap.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .member import member as member_blueprint
    app.register_blueprint(member_blueprint, url_prefix='/member')
    if add_fake:
        fake_data()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
