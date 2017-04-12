# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email
from flask_pagedown.fields import PageDownField


class UserForm(FlaskForm):
    user_name = StringField(u"User name",
                            validators=[Length(1, 64)], id="user_name")
    submit = SubmitField(u"Change username", id="Submit")


class PostForm(FlaskForm):
    title = StringField(u"Title",
                        validators=[Length(1, 100)], id="title")
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField(u"Submit Markdown", id="Submit")


class CommentForm(FlaskForm):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField(u"Submit Markdown", id="Submit")
