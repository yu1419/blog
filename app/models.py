#coding: utf-8
from . import db


class PostModel():

    def breif_post(self, start=0, total=5, id = None):
        sql = """ select title, content from post limit %s, %s"""
        result = ""
        with db.cursor() as cursor:
            cursor.execute(sql, (start, total))
            result = cursor.fetchall()
            post = []
            for item in result:
                title = item[0]
                content = item[1][:100]
                post.append((title, content))
        return post

    def by_id(self, id):
        sql = """ select title, content from post where post_id = %s"""
        result = ""
        with db.cursor() as cursor:
            cursor.execute(sql, (id))
            result = cursor.fetchall()
            post = []
            title = item[0]
            content = item[1][:100]
            post.append((title, content))
        return post
