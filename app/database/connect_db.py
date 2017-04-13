
import pymysql
import os


def get_db():
    """connect to mysql database, return db"""
    db = pymysql.connect(os.environ["mysql_host"], os.environ["mysql_username"], os.environ["mysql_password"],
                         "blog", charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    return db

db = get_db()
db.close()
