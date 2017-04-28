# coding: utf-8
from . import db, get_db
from flask_login import UserMixin, AnonymousUserMixin
from .generate_password import general_random_password, valid_login
from werkzeug.security import generate_password_hash

# show 5 blogs per page
count_per_page = 5


class AnonymousUser(AnonymousUserMixin):
    global db
    db = get_db()

    def show_articles(self, page=1):
        # show index page articles, which contains blogs posted by everyone
        ignore = (page - 1) * count_per_page
        sql = "select * from post, user where user.user_id = post.user_id \
               order by post_time DESC limit %s, %s"
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles

    def is_following(self, user_id):
        # do not follow anybody
        return False

    def reset_email(self, email):
        # user is not logged in, system can generate a random password
        # and then sent to email address entered
        password, hashed_password = general_random_password()
        sql = "update user set hashed_password = %s where email = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (hashed_password, email))
            db.commit()
            return password


class UserBase(object):
    global db
    db = get_db()
    def __init__(self, id):
        # initial userbase by email, because user use email to log in
        self.id = id
        self._update_userid()  # get user_id

    def _update_userid(self):
        sql = "select user_id from user where email = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.id, ))
            self.user_id = cursor.fetchone()["user_id"]

    def post_count(self):
        # get total post of user
        sql = "select count(*) from post where user_id = %s"
        result = 0
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id))
            result = cursor.fetchone()["count(*)"]
        return result

    def info(self):
        # get related information of user

        sql = "select * from user where user_id = %s"
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ))
            result = cursor.fetchone()
        return result

    def get_post(self, post_id):
        # get user post by post id
        sql = "select * from post where user_id = %s and post_id = %s"
        result = None
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, post_id))
            result = cursor.fetchone()
        return result

    def update_post(self, post_id, title, content):
        sql = "update post set title = %s, content = %s \
               where user_id = %s and post_id = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (title, content, self.user_id, post_id))
            db.commit()

    def add_comment(self, reply_to_id, post_id, comment_content):
        # add comment to a post
        sql = "insert into comment (user_id, reply_to_id, post_id, \
               comment_content) values(%s, %s, %s, %s)"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, reply_to_id,
                                 post_id, comment_content))
            db.commit()

    def name_available(self, new_name):
        # check if a user name already exists or not
        sql = "select count(*) from user where user_name = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (new_name,))
            if cursor.fetchone()["count(*)"]:
                return False
            else:
                return True

    def update_info(self, new_name, about_me):
        # update user name and about information
        available = self.name_available(new_name)
        if available:
            sql = "UPDATE user set user_name = %s, about_me = %s \
                   where user_id = %s"
            with db.cursor() as cursor:
                cursor.execute(sql, (new_name, about_me, self.user_id))
                db.commit()
                return True
        else:
            if not new_name == self.info()["user_name"]:
                return False
            else:
                return True

    def add_post(self, title, content):
        # write a blog
        sql = "insert into post (title, content, user_id) values(%s, %s, %s)"
        with db.cursor() as cursor:
            cursor.execute(sql, (title, content, self.user_id))
            db.commit()
            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql)
            row_id = cursor.fetchone()["LAST_INSERT_ID()"]
            return row_id

    def follow(self, other_id):
        # follow a user by user id
        sql = "insert into follow (user_id, follower) values (%s, %s)"
        result = False
        with db.cursor() as cursor:
            cursor.execute(sql, (other_id, self.user_id))
            db.commit()
            result = True
        return result

    def un_follow(self, other_id):
        # unfollow a user by user_id
        sql = "delete from follow where user_id = %s and follower = %s"
        result = False
        with db.cursor() as cursor:
            cursor.execute(sql, (other_id, self.user_id))
            db.commit()
            result = True
        return result

    def follower_id(self):
        # all users that are following current user
        ids = []
        sql = "select follower from follow where user_id = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ))
            result = cursor.fetchall()
            for item in result:
                ids.append(item["follower"])
        return ids

    def is_following(self, user_id):
        # current user is following user with a specific user_id
        return user_id in self.followed_id()

    def followed_id(self):
        # users that are followed by current_user
        ids = []
        sql = "select user_id from follow where follower = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ))
            result = cursor.fetchall()
            for item in result:
                ids.append(item["user_id"])
        return ids

    def delete_post(self, post_id):
        # delete a post by post_id
        sql = "delete from post where user_id = %s and post_id = %s"
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, post_id))
            db.commit()

    def own_articles(self, page=1):
        # return a lost of blogs posted by current_user
        ignore = (page - 1) * count_per_page
        sql = "select * from post, user where post.user_id = %s and post.user_id=\
               user.user_id order by post_time DESC limit %s, %s"
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (self.user_id, ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles

    def show_articles(self, page=1):
        # show posts of all users
        ignore = (page - 1) * count_per_page
        sql = "select * from post, user where user.user_id = post.user_id \
               order by post_time DESC limit %s, %s"
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles

    def show_followed_articles(self, page=1):
        # show posts that created by users followed by current_user
        followeds = self.followed_id()
        followeds = " or ".join(["post.user_id=%s" % i for i in followeds])
        restriction = "where " + "(" + followeds + ")"

        ignore = (page - 1) * count_per_page
        sql = "select * from post, user {} and post.user_id=user.user_id \
               order by post_time DESC limit %s, %s".format(restriction)
        articles = []
        with db.cursor() as cursor:
            cursor.execute(sql, (ignore, count_per_page))
            result = cursor.fetchall()
            if result:
                articles = result
        return articles

    def change_password(self, old, new):
        # change user password
        valid = valid_login(self.id, old)  # id is email
        if valid:
            new = generate_password_hash(new)
            sql = "update user set hashed_password = %s where user_id = %s"
            with db.cursor() as cursor:
                cursor.execute(sql, (new, self.user_id))
                db.commit()
                return True

        else:
            return False


class User(UserBase, UserMixin):
    pass


class Single_post_model(object):
    global db
    db = get_db()
    def __init__(self, post_id):
        self.post_id = post_id

    def get_comments(self):
        # get all comments of current post
        sql = "select * from comment, user where post_id = %s \
              and comment.user_id = user.user_id order by comment_time DESC"
        result = []
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id, ))
            comment_ids = cursor.fetchall()
            if comment_ids:
                result = comment_ids
        return result

    def get_info(self):
        # get post infor and user info
        sql = "select * from post, user where post_id = %s and \
               post.user_id = user.user_id"
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql, (self.post_id, ))
            result = cursor.fetchone()
        return result
