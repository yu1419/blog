from . import auth
from .forms import LoginForm, Register, Rest_password, Change_password
from flask_login import login_user, logout_user, current_user, login_required
from ..models import User
from ..helper import get_user, valid_login, email_exist, register_user, \
                     send_email
from .. import login_manager, mail
from flask_mail import Message
from flask import redirect, flash, render_template, url_for, current_app


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        exist = email_exist(email)
        if exist:
            flash("email registered", "bad")
            return redirect(url_for(".register"))
        register_user(email, password)
        return redirect(url_for("main.index"))
    return render_template("single_form.html", form=form, title="Register")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logout", "good")
    return redirect(url_for("main.index"))


@auth.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    form = Rest_password()
    if form.validate_on_submit():
        email = form.email.data
        has_email = email_exist(email)
        if has_email:
            new_password = current_user.reset_email(email)
            msg = Message("Your new password of blog website",
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.html = render_template("new_password.html",
                                       new_password=new_password)
            send_email(mail, msg)
            flash("A temporary password has been sent to your email", "good")
            return redirect(url_for(".login"))
        else:
            flash("email doesn't exist", "bad")
    return render_template("single_form.html", form=form,
                           title="Reset password")


@auth.route("/change_password", methods=['GET', 'POST'])
def change_password():
    form = Change_password()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.password.data
        result = current_user.change_password(old_password, new_password)
        if result:
            flash("You have changed your password", "good")
            return redirect(url_for("main.profile",
                            user_id=current_user.user_id))
        else:
            flash("old email is not correct", "bad")
    return render_template("single_form.html", form=form,
                           title="Change password")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        valid = valid_login(email, password)
        if valid:
            user = User(email)
            login_user(user, remember_me)
            flash("Sucess", "good")
            return redirect(url_for("main.index"))
        else:
            flash("Failed", "bad")
            return redirect(url_for(".login"))
    return render_template("single_form.html", form=form, title="Login")
