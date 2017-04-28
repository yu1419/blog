import string
import random
from . import get_db
from werkzeug.security import generate_password_hash, check_password_hash


def general_random_password(n=10):
    # generate a password with a length of 10
    char_list = string.ascii_uppercase + string.digits
    pass_list = [random.choice(char_list) for _ in range(n)]
    password = "".join(pass_list)
    hashed_password = generate_password_hash(password)
    return password, hashed_password


def valid_login(email, password):
    # check if a log in if valid or not
    sql = "select hashed_password from user where email = %s"
    hashed_password = ""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            hashed_password = result.get("hashed_password", "")
    db.close()
    if check_password_hash(hashed_password, password):
        return True
    else:
        return False
