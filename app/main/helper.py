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


def user_basic(user_id):
    sql = "select * from user where user_id = %s"
    result = None
    with db.cursor() as cursor:
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
    return result
