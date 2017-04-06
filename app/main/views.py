from . import main
from ..models import PostModel, Comment_model
from flask import render_template
a = PostModel()


@main.route("/")
def index():
    result = a.breif_post()
    return render_template("index.html", result=result)


@main.route("/more_index")
def more_index():
    pass


@main.route("/user=<int:user_id>")
def user_post(user_id):
    result = a.by_user(user_id)
    return str(result)


@main.route("/more_user")
def more_user():
    pass


@main.route("/home")
def home(user_id):
    result = a.by_user(user_id)
    return str(result)


@main.route("/more_home")
def more_home():
    pass


@main.route("/post_id=<int:post_id>")
def post_byID(post_id):
    result = a.by_postID(post_id)
    b = Comment_model(post_id)
    return str(result)
