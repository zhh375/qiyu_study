import sqlite3
from common.public import print_format

def create_table(db_name, sql):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print_format(e, 'red')
        return False


def insert_data(db_name, sql):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print_format(e, 'red')
        return False


def select_data(db_name, sql):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cursor = cur.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print_format(e, 'red')
        return False


def update_data(db_name, sql):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print_format(e, 'red')
        return False


def delete_data(db_name, sql):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print_format(e, 'red')
        return False