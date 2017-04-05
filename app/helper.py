import string
import random


def general_random_password(n=50):
    char_list = string.ascii_uppercase + string.digits
    pass_list = [random.choice(char_list) for _ in range(n)]
    password = "".join(pass_list)
    return password
