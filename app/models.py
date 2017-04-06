# coding: utf-8
from . import db
from .helper import general_random_password
from pymysql.cursors import DictCursor as Dic
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class UserBase(object):
    def __init__(self, id):
        self.id = id  # id is email
        self.update_userid()

    def update_userid(self):
        sql = "select user_id from user where email = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.id, ))
            self.user_id = cursor.fetchone()["user_id"]

    def follower_id(self):
        ids = []
        sql = "select follower from follow where user_id = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ))
            result = cursor.fetchall()
            for item in result:
                ids.append(item["follower"])
        return ids

    def followed_id(self):
        ids = []
        sql = "select user_id from follow where follower = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ))
            result = cursor.fetchall()
            for item in result:
                ids.append(item["user_id"])
        return ids


class User(UserBase, UserMixin):
    pass


class PostModel(object):

    def breif_post(self, start=0, total=5, id=None):
        sql = """ select * from post limit %s, %s"""
        with db.cursor() as cursor:
            cursor.execute(sql, (start, total))
            post = cursor.fetchall()
        return post

    def by_user(self, id):
        sql = """ select * from post where user_id = %s"""
        post = ""
        with db.cursor() as cursor:
            cursor.execute(sql, (id))
            post = cursor.fetchall()
        return post

    def by_postID(self, id):
        sql = """ select * from post where post_id = %s"""
        post = []
        with db.cursor() as cursor:
            cursor.execute(sql, (id))
            post = cursor.fetchone()
        return post


class Comment_model(object):
    def __init__(self, post_id):
        self.post_id = post_id

    def all_comments(self):
        sql = """ select * from comment where post_id = %s"""
        comment = []
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id))
            comment = cursor.fetchone()
        return comment

    def add_comment(self, user_id, content, reply_to=None):
        sql = "insert into comment (user_id, reply_to_id, comment_content, post_id)\
              values(%s, %s, %s, %s)"
        with db.cursor() as cursor:
            cursor.execute(sql, (user_id, reply_to, content, self.post_id))
            db.commit()


class Register_model(object):
    def check_email(self, email):
        sql = "select count(*) from user where email = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (email,))
            return cursor.fetchone()["count(*)"]

    def check_username(self, name):
        sql = "select count(*) from user where user_name = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (name,))
            return cursor.fetchone()["count(*)"]

    def register(self, username, email, password):
        has_email = self.check_email(email)
        has_name = self.check_username(username)
        message = ""
        if has_email:
            message = "Email has already been registered\t"
        if has_name:
            message += "Username has already been registered"
        if len(message) == 0:
            hashed_password = generate_password_hash(password)
            sql = "insert into user (user_name, email, hashed_password) \
                  values(%s, %s, %s)"
            with db.cursor() as cursor:
                cursor.execute(sql, (username, email, hashed_password))
                db.commit()
        return message
