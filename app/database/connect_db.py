
import pymysql
import os


def get_db():
    """connect to mysql database, return db"""
    db = pymysql.connect("localhost", "root", os.environ["mysql_password"],
                         "blog", charset='utf8')
    return db

db = get_db()
db.close()
