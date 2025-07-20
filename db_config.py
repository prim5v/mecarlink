import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host='themmwaks.mysql.pythonanywhere-services.com',
        user='themmwaks',
        password='modcom1234',
        database='themmwaks$test',
        cursorclass=pymysql.cursors.DictCursor
    )

