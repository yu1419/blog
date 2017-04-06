from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User


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
