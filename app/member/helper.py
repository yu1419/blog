from .. import db


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
