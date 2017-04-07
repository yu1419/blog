# coding: utf-8
from . import db
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
count_per_page = 5


class AnonymousUser(AnonymousUserMixin):
    def show_articles(self, page=1):
        ignore = (page - 1) * count_per_page
        sql = "select * from post order by post_time DESC limit %s, %s"
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles


class UserBase(object):
    def __init__(self, id):
        self.id = id  # id is email
        self._update_userid()

    def _update_userid(self):
        sql = "select user_id from user where email = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.id, ))
            self.user_id = cursor.fetchone()["user_id"]

    def info(self):
        sql = "select * from user where user_id = %s"
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ))
            result = cursor.fetchone()
        return result

    def update_username(self, new_name):
        sql = "update user set user_name = %s where user_id = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (new_name, self.user_id))
            db.commit()



    def follow(self, other_id):
        sql = "insert into follow (user_id, follower) values (%s, %s)"
        result = False
        with db.cursor() as cursor:
            cursor.execute(sql, (other_id, self.user_id))
            db.commit()
            result = True
        return result

    def un_follow(self, other_id):
        sql = "delete from follow where user_id = %s and follower = %s"
        result = False
        with db.cursor() as cursor:
            cursor.execute(sql, (other_id, self.user_id))
            db.commit()
            result = True
        return result

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

    def add_comment(self, post_id, reply_to, content):
        pass

    def own_articles(self, page=1):
        ignore = (page - 1) * count_per_page
        sql = "select * from post where user_id = %s order by \
               post_time DESC limit %s, %s"
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles

    def show_articles(self, page=1):
        ignore = (page - 1) * count_per_page
        sql = "select * from post order by post_time DESC limit %s, %s"
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles

    def show_followed_articles(self, page=1):
        followeds = self.followed_id()
        followeds = " or ".join(["user_id=%s" % i for i in followeds])
        restriction = "where " + followeds

        ignore = (page - 1) * count_per_page
        sql = "select * from post {} order by post_time DESC limit %s, %s".format(restriction)
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles




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
    def __init__(self, post_id):
        self.post_id = post_id

    def get_comments(self):
        sql = "select comment_id from comment where post_id = %s \
              order by comment_time DESC"
        result = []
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id, ))
            comment_ids = cursor.fetchall()
            if comment_ids:
                result = comment_ids
        return result

    def get_info(self):
        sql = "select * from post where post_id = %s"
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id, ))
            result = cursor.fetchone()
        return result

login_manager.anonymous_user = AnonymousUser
