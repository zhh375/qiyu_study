import time
from common.public import print_format
from common.sqlite_rw import create_table, insert_data
import os


db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db/qiyu.db")


def init_db():
    if not os.path.exists(db_path):
        print_format("db目录不存在，创建db", "yellow")
        create_table(db_path,
                     "CREATE TABLE IF NOT EXISTS cn_word ("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "name TEXT, "
                            "category INTEGER, "
                            "user TEXT, "
                            "status INTEGER, "
                            "create_time INTEGER, "
                            "update_time INTEGER)")
        insert_data(db_path,
                    "INSERT INTO cn_word (id, name, category, user, status, create_time, update_time) "
                    "VALUES (0, '开始', 1, '琦琦', 0, {}, 0)".format(int(time.time())))

        create_table(db_path,
                     "CREATE TABLE IF NOT EXISTS en_word ("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "name TEXT, "
                            "category INTEGER, "
                            "user TEXT, "
                            "status INTEGER, "
                            "parent_id INTEGER, "
                            "create_time INTEGER, "
                            "update_time INTEGER)")
        insert_data(db_path,
                    "INSERT INTO cn_word (id, name, category, user, status, parent_id, create_time, update_time) "
                    "VALUES (0, 'start', 1, '琦琦', 0, 0, {}, 0)".format(int(time.time())))
        insert_data(db_path,
                    "INSERT INTO cn_word (id, name, category, user, status, parent_id, create_time, update_time) "
                    "VALUES (1, 'I like ', 1, '琦琦', 0, 0, {}, 0)".format(int(time.time())))
        insert_data(db_path,
                    "INSERT INTO cn_word (id, name, category, user, status, parent_id, create_time, update_time) "
                    "VALUES (2, 'english', 1, '琦琦', 0, 1, {}, 0)".format(int(time.time())))

