import mysql.connector
import datetime
from . import config

def connect():
    try:
        conn = mysql.connector.connect(
            host=config.mysqlHost,
            user=config.mysqlUser,
            password=config.mysqlPassword,
            database=config.mysqlDB
        )
        return conn
    except Exception as error:
        print("Ошибка подключения к базе данных: {}".format(error))
        return None

#########################################################################################################################################################################

class add:
    def user(userId, fullName):
        conn = connect()
        cursor = conn.cursor()

        sql = 'INSERT INTO users(userId, fullName, regDate) VALUES (%s, %s, %s)'
        params = [userId, fullName, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')]

        cursor.execute(sql, params)
        conn.commit()

#########################################################################################################################################################################

class exist:
    def blockedUser(userId):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT isBlocked FROM users WHERE userId = '{userId}'")
        statusBlocked = cursor.fetchone()[0]
        if bool(statusBlocked):
            return True
        else:
            return False
        
    def user(userId):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT userId FROM users WHERE userId = '{userId}'")
        if cursor.fetchone() is None:
            return False
        else:
            return True

#########################################################################################################################################################################

def getUser(userId):
    conn = connect()
    cursor = conn.cursor()

    sql = 'SELECT * FROM users WHERE userId = %s'
    params = [userId]

    cursor.execute(sql, params)
    row = cursor.fetchone()
    return row

#########################################################################################################################################################################

def updateUserName(userId, fullName):
    conn = connect()
    cursor = conn.cursor()

    sql = 'UPDATE users SET fullName = %s WHERE userId = %s'
    params = [fullName, userId]

    cursor.execute(sql, params)
    conn.commit()