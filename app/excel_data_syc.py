from common.excel_read import read_excel
from common.sqlite_rw import insert_data, select_data
import time
import os


def cn_word_syc(file_path):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db/qiyu.db")
    data = read_excel(file_path)
    for row in data:
        select_sql = ("select id from cn_word where name='{}'".format(row["name"]))
        select_name = select_data(db_path, select_sql)
        if select_name:
            continue
        insert_sql = ("insert into cn_word(name, category, user, status, create_time, update_time) "
                      "values('{}', {}, '{}', {}, {}, 0)"
                      .format(row["name"], row["category"], row["user"], row["status"], int(time.time())))
        if insert_data(db_path, insert_sql) is False:
            return False

    return True

