from . import member
from ..models import PostModel
from flask import render_template, redirect, url_for
from .. import login_required
from flask_login import current_user
from .forms import UserForm, PostForm


@login_required
@member.route("/follow/<int:user_id>", methods=['GET', 'POST'])
def follow(user_id):
    result = current_user.follow(user_id)
    return str(result)


@login_required
@member.route("/un_follow/<int:user_id>", methods=['GET', 'POST'])
def un_follow(user_id):
    result = current_user.un_follow(user_id)
    return str(result)


@login_required
@member.route("/new_post", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        row_id = current_user.add_post(title, form.pagedown.data)
        return redirect(url_for("main.post_byID", post_id=row_id))
    return render_template("search.html", form=form)


@login_required
@member.route("/profile", methods=['GET', 'POST'])
def profile():
    info = current_user.info()
    user_name = info["user_name"]
    # email = info["email"]
    form = UserForm(user_name=user_name)
    if form.validate_on_submit():
        current_user.update_username(form.user_name.data)
    return render_template("search.html", form=form)
