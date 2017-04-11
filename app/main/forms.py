# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email
from flask_pagedown.fields import PageDownField


class CommentForm(FlaskForm):
    pagedown = PageDownField('')
    submit = SubmitField(u"Submit", id="Submit")
