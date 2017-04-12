from . import main
from ..models import Single_post_model, UserBase
from flask import render_template, session, jsonify, redirect, url_for,\
                  flash, request
from flask_login import current_user
from ..helper import convert_id, user_basic, id_to_username, name_to_id
from .forms import CommentForm, UserForm


@main.route("/")
def index():
    session["page"] = 1
    result = current_user.show_articles()
    return render_template("index.html", result=result, title="All blogs")


@main.route("/more_index")
def more_index():
    page = session.get("page", 0)
    session["page"] = page + 1
    current_page = session["page"]
    #  articles = {}
    result = current_user.show_articles(current_page)
    return render_template("more.html", result=result)
    #  return jsonify(articles)


@main.route("/user_basic/<int:user_id>")
def user_basic_into(user_id):
    result = user_basic(user_id)
    return jsonify(result)


@main.route("/user/<int:user_id>")
def user_post(user_id):
    name = id_to_username(user_id)
    email = convert_id(user_id)
    session["user_page"] = 1

    user = UserBase(email)
    session["user_articles"] = email
    result = user.own_articles()
    return render_template("index.html", result=result, user_id=user_id,
                           title=name + "\' Posts")


@main.route("/more_user")
def more_user():
    page = session.get("user_page", 0)
    session["user_page"] = page + 1
    current_page = session["user_page"]
    email = session["user_articles"]

    user = UserBase(email)
    result = user.own_articles(current_page)
    return render_template("more.html", result=result)


@main.route("/home")
def home():
    session["home_page"] = 1
    articles = current_user.show_followed_articles()
    return render_template("index.html", result=articles, title="Home")


@main.route("/more_home")
def more_home():
    page = session.get("home_page", 0)
    session["home_page"] = page + 1
    current_page = session["home_page"]
    result = current_user.show_followed_articles(current_page)
    return render_template("more.html", result=result)


@main.route("/post_id/<int:post_id>", methods=['GET', 'POST'])
def post_byID(post_id):
    post = Single_post_model(post_id)
    info = post.get_info()
    info["comments"] = post.get_comments()
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            reply_to_name = (request.form.get("reply_to_name", None))
            reply_to_id = name_to_id(reply_to_name)
            current_user.add_comment(reply_to_id=reply_to_id, post_id=post_id,
                                     comment_content=form.pagedown.data)
            return redirect(url_for(".post_byID", post_id=post_id))
        else:
            flash("Please sign in to commment")
    return render_template("single_post.html", form=form, post=info)


@main.route("/profile/<int:user_id>", methods=['GET', 'POST'])
def profile(user_id):
    if current_user.is_authenticated and \
          current_user.info()["user_id"] == user_id:
        user_name = current_user.info()["user_name"]
        form = UserForm(user_name=user_name)
        if form.validate_on_submit():
            result = current_user.update_username(form.user_name.data)
            if result:
                flash("Username changed", "good")
            else:
                flash("Username already exists", "bad")
                return redirect(url_for(".profile"))
        return render_template("single_form.html", form=form, title="Profile")
    else:
        user_email = convert_id(user_id)
        author = UserBase(user_email)
        info = author.info()
        user_name = info.get("user_name")
        return render_template("profile.html", user_name=user_name,
                               title="Profile")
