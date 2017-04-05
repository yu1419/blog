# coding: utf-8
from . import db
from pymysql.cursors import DictCursor as Dic

class PostModel():

    def breif_post(self, start=0, total=5, id=None):
        sql = """ select * from post limit %s, %s"""
        result = ""
        with db.cursor() as cursor:
            cursor.execute(sql, (start, total))
            post = cursor.fetchall()
        return post

    def by_user(self, id):
        sql = """ select * from post where user_id = %s"""
        result = ""
        with db.cursor() as cursor:
            cursor.execute(sql, (id))
            post = cursor.fetchall()
        return post

    def by_postID(self, id):
        sql = """ select * from post where post_id = %s"""
        post = []
        with db.cursor() as cursor:
            cursor.execute(sql, (id))
            post = cursor.fetchone()
        return post
