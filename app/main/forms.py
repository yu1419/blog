# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email
from flask_pagedown.fields import PageDownField


class CommentForm(FlaskForm):
    pagedown = PageDownField('')
    submit = SubmitField(u"Submit", id="Submit")


class UserForm(FlaskForm):
    user_name = StringField(u"User name",
                            validators=[Length(1, 64)], id="user_name")
    submit = SubmitField(u"Change username", id="Submit")
