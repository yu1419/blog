# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email


class LoginForm(FlaskForm):
    email = StringField(u'Email', validators=[Length(1, 64),
                                              Email()], id="email")
    password = PasswordField(u'Password',
                             validators=[Length(6, 64)], id="password")
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField(u"Submit", id="Submit")


class Register(FlaskForm):
    email = StringField(u'Email', validators=[Length(1, 64),
                                              Email()], id="email")
    password = PasswordField(u'Password',
                             validators=[Length(6, 64)], id="password")
    submit = SubmitField(u"Register", id="Submit")


class Change_password(FlaskForm):
    old_password = PasswordField(u'Old password',
                                 validators=[Length(6, 64)], id="password")
    password = PasswordField(u'New Password',
                             validators=[Length(6, 64)], id="password")
    submit = SubmitField(u"Change Password", id="Submit")


class Rest_password(FlaskForm):
    email = StringField(u'Email', validators=[Length(1, 64),
                                              Email()], id="email")
    submit = SubmitField(u"Send password to email", id="Submit")
