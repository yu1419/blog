from . import auth
from .forms import LoginForm, Register
from flask_login import login_user, logout_user, current_user
from ..models import User
from .helper import get_user, valid_login, email_exist, register_user
from .. import login_manager, login_required
from flask import redirect, flash, render_template, url_for


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
