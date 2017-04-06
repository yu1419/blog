# coding: utf-8
from . import db
from .helper import general_random_password
from pymysql.cursors import DictCursor as Dic
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class UserBase(object):
    def __init__(self, id):
        self.id = id  # id is email
        self._update_userid()

    def _update_userid(self):
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

    def un_follow(self, follow_id):
        sql = "delete from follow where follower = %s and user_id = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (follow_id, self.user_id))
            cursor.commit()

    def follow(self, follow_id):
        sql = "insert into follow (follower, user_id ) values (%s, %s)"
        with db.cursor() as cursor:
            cursor.execute(sql, (follow_id, self.user_id))
            db.commit()

    def add_comment(self, post_id, reply_to, content):
        pass

    def show_articles(self):
        pass

    def show_follower_articles(self):
        pass


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
    def __init__(self, comment_id):
        self. comment_id = comment_id

    def get_info(self):
        pass


class Single_post_model(object):
    def __int__(self, post_id):
        self.post_id = self.post_id

    def get_comment(self):
        sql = "select comment_id from comment where post_id = %s \
              order by comment_time DESC"
        result = []
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id, ))
            comment_ids = cursor.fetchall()
            if comment_ids:
                for comment_id in comment_ids:
                    result.append(comment_id.get("comment_id"))
        return result

    def get_info(self):
        sql = "select * from post where post_id = %s"
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id, ))
            result = cursor.fetchone()
        self.title = result.get("title")
        self.content = result.get("content")
        self.post_time = result.get("post_time")
        self.last_modified = result.get("last_modified")
