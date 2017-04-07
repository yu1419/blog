from . import main
from ..models import Single_post_model, UserBase
from flask import render_template, session
from flask_login import current_user
from .helper import convert_id


@main.route("/")
def index():
    session["page"] = 1
    result = current_user.show_articles()
    return render_template("index.html", result=result)


@main.route("/more_index")
def more_index():
    page = session.get("page", 0)
    session["page"] = page + 1
    current_page = session["page"]
    articles = current_user.show_articles(current_page)
    return str(articles)


@main.route("/user/<int:user_id>")
def user_post(user_id):
    email = convert_id(user_id)
    session["user_page"] = 1
    user = UserBase(email)
    session["user_articles"] = email
    result = user.own_articles()
    return str(result)


@main.route("/user/more_user")
def more_user():
    page = session.get("user_page", 0)
    session["user_page"] = page + 1
    current_page = session["user_page"]
    email = session["user_articles"]
    user = UserBase(email)
    articles = user.own_articles(current_page)
    return str(articles)


@main.route("/home")
def home():
    session["home_page"] = 1
    articles = current_user.show_followed_articles()
    return str(articles)


@main.route("/more_home")
def more_home():
    page = session.get("home_page", 0)
    session["home_page"] = page + 1
    current_page = session["home_page"]
    articles = current_user.show_followed_articles(current_page)
    return str(articles)


@main.route("/post_id/<int:post_id>")
def post_byID(post_id):
    post = Single_post_model(post_id)
    info = post.get_info()
    info["comment"] = post.get_comments()
    return str(info)
