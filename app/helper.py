from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from threading import Thread
from flask import current_app


def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_email(mail, msg):
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, mail, msg])
    thr.start()
    return thr


def register_user(email, password):
    hashed_password = generate_password_hash(password)
    sql = "insert into user (user_name, email, hashed_password) \
           values (%s, %s, %s)"
    with db.cursor() as cursor:
        cursor.execute(sql, (email, email, hashed_password))
        db.commit()


def email_exist(email):
    sql = "select count(*) from user where email = %s"
    count = 0
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            count = result.get("count(*)", "")
    if count:
        return True
    else:
        return False


def valid_login(email, password):
    sql = "select hashed_password from user where email = %s"
    hashed_password = ""
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            hashed_password = result.get("hashed_password", "")
    if check_password_hash(hashed_password, password):
        return True
    else:
        return False


def get_user(email):
    user = None
    sql = "select count(*) from user where email = %s"
    count = 0
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            count = result.get("count(*)", 0)
    if count:
        user = User(email)
    return user


def convert_id(id):
    sql = "select email from user where user_id = %s"
    email = ""
    with db.cursor() as cursor:
        cursor.execute(sql, id)
        result = cursor.fetchone()
        if result:
            email = result["email"]
    return email


def id_to_username(user_id):
    sql = "select user_name from user where user_id = %s"
    user_name = None
    with db.cursor() as cursor:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        if result:
            user_name = result["user_name"]
    return user_name


def name_to_id(user_name):
    if not user_name:
        return None
    sql = "select user_id from user where user_name = %s"
    user_id = None
    with db.cursor() as cursor:
        cursor.execute(sql, user_name)
        result = cursor.fetchone()
        if result:
            user_id = result["user_id"]
    print(user_id)
    return user_id


def user_basic(user_id):
    sql = "select * from user where user_id = %s"
    result = None
    with db.cursor() as cursor:
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
    return result
