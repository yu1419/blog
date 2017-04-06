import string
import random
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


def general_random_password(n=50):
    char_list = string.ascii_uppercase + string.digits
    pass_list = [random.choice(char_list) for _ in range(n)]
    password = "".join(pass_list)
    return password


def valid_login(email, password):
    sql = "select hashed_password from user where email = %s"
    hashed_password = ""
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        hashed_password = cursor.fetchone().get("hashed_password", "")
    if check_password_hash(hashed_password, password):
        return True
    else:
        return False
