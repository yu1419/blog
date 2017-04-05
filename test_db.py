from app.database.connect_db import get_db
import time


db = get_db()
while True:
    sql = "select count(*) from post"
    with db.cursor() as cursor:
        cursor.execute(sql)
        print(str(cursor.fetchall()))
    time.sleep(10)

db.close()
