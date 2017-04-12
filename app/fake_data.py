import forgery_py
from .database import db
from werkzeug.security import generate_password_hash
import random

#  important !!
#  add to lorem_ipsum.py    :
# import sys
# if sys.version_info.major >= 3:xrange = range


USER_count = 100
POST_COUNT = 1000
COMMENT_COUNT = 10
FOLLOW_COUNT = 100


def fake_user(USER_count=100):
    for i in range(USER_count):
        user_name = forgery_py.name.full_name()
        email = forgery_py.internet.email_address()
        hashed_password = generate_password_hash(email)
        sql = "insert into user (user_name, email, hashed_password) \
               values (%s, %s, %s)"
        try:
            with db.cursor() as cursor:
                cursor.execute(sql, (user_name, email, hashed_password))
                db.commit()
        except Exception as e:
            print(e)


def fake_post(POST_COUNT=1000):
    all_user_id = []
    sql = "select user_id from user"
    with db.cursor() as cursor:
        cursor.execute(sql)
        all_user_id = cursor.fetchall()
    for i in range(POST_COUNT):
        user_id_index = random.randrange(len(all_user_id))
        user_id = all_user_id[user_id_index]["user_id"]
        title = forgery_py.lorem_ipsum.title()
        content = forgery_py.forgery.lorem_ipsum.\
            paragraphs(quantity=3, sentences_quantity=4)
        sql = "insert into post (user_id, title, content) \
               values (%s, %s, %s)"
        try:
            with db.cursor() as cursor:
                cursor.execute(sql, (user_id, title, content))
                db.commit()
        except Exception as e:
            print(e)


def fake_follow(FOLLOW_COUNT = 100):
    all_user_id = []
    sql = "select user_id from user"
    with db.cursor() as cursor:
        cursor.execute(sql)
        all_user_id = cursor.fetchall()
    for user in all_user_id:
        for i in range(FOLLOW_COUNT):
            user_id_index = random.randrange(len(all_user_id))
            follower = all_user_id[user_id_index]["user_id"]
            user_id = user["user_id"]
            sql = "insert into follow (user_id, follower) \
                   values (%s, %s)"
            try:
                with db.cursor() as cursor:
                    cursor.execute(sql, (user_id, follower))
                    db.commit()
            except Exception as e:
                print(e)


def fake_comment(COMMENT_COUNT=10):
    all_user_id = []
    all_post_id = []
    sql = "select user_id from user"
    with db.cursor() as cursor:
        cursor.execute(sql)
        all_user_id = cursor.fetchall()
    sql = "select post_id from post"
    with db.cursor() as cursor:
        cursor.execute(sql)
        all_post_id = cursor.fetchall()

    for post in all_post_id:
        for i in range(COMMENT_COUNT):
            post_id = post["post_id"]
            user_id_index = random.randrange(len(all_user_id))
            user_id = all_user_id[user_id_index]["user_id"]
            do_reply_to = random.choice([True, False])
            reply_to_id = None
            if do_reply_to:
                user_id_index = random.randrange(len(all_user_id))
                reply_to_id = all_user_id[user_id_index]["user_id"]
            user_id_index = random.randrange(len(all_user_id))
            user_id = all_user_id[user_id_index]["user_id"]
            comment_content = forgery_py.forgery.lorem_ipsum.sentence()
            sql = "insert into comment (post_id, user_id, reply_to_id,\
                   comment_content) values (%s, %s, %s, %s)"
            try:
                with db.cursor() as cursor:
                    cursor.execute(sql, (post_id, user_id, reply_to_id,
                                         comment_content))
                    db.commit()
            except Exception as e:
                print(e)


def fake_data():
    fake_user()
    fake_follow()
    fake_post()
    fake_comment()
