# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email


class UserForm(FlaskForm):
    user_name = StringField(u"user name",
                            validators=[Length(1, 64)], id="user_name")
    submit = SubmitField(u"Submit", id="Submit")
