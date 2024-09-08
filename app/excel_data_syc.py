from common.excel_read import read_excel
from common.sqlite_rw import insert_data
import os


def cn_word_syc(file_path):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db/qiyu.db")
    data = read_excel(file_path)
    for row in data:
        insert_sql = ("insert into cn_word(name, category, user, status, create_time) values('{}', {}, '{}', {})"
                      .format(row[0], row[1], row[2], row[3]))
        if insert_data(db_path, insert_sql) is False:
            return False

    return True

