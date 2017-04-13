from . import member
from flask import render_template, redirect, url_for, abort, \
                  flash, request
from flask_login import current_user, login_required
from .forms import PostForm
from ..helper import id_to_username


@member.route("/delete/<int:post_id>", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    current_user.delete_post(post_id)
    return redirect(request.referrer)


@member.route("/follow/<int:user_id>", methods=['GET', 'POST'])
def follow(user_id):
    if current_user.is_authenticated:
        current_user.follow(user_id)
        followed = str(id_to_username(user_id))
        flash("You followed {}".format(followed), "good")
        return redirect(request.referrer)
    else:
        flash("please log in to follow users", "bad")
        return redirect(request.referrer)


@member.route("/un_follow/<int:user_id>", methods=['GET', 'POST'])
def un_follow(user_id):
    current_user.un_follow(user_id)
    unfollowed = str(id_to_username(user_id))
    flash("You unfollowed {}".format(unfollowed), "good")
    return redirect(request.referrer)


@member.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        row_id = current_user.add_post(title, form.pagedown.data)
        return redirect(url_for("main.post_byID", post_id=row_id))
    return render_template("single_form.html", form=form, title="New Post")


@login_required
@member.route("/edit_post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    current_post = current_user.get_post(post_id)
    if not current_post:
        abort(404)
    form = PostForm(title=current_post["title"],
                    pagedown=current_post["content"])
    if form.validate_on_submit():
        title = form.title.data
        current_user.update_post(current_post["post_id"],
                                 title, form.pagedown.data)
        return redirect(url_for("main.post_byID",
                        post_id=current_post["post_id"]))
    return render_template("single_form.html", form=form, title="Edit Post")
