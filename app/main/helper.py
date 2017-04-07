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
