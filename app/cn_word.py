from common.sqlite_rw import select_data, delete_data, insert_data, update_data
import os


db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db/qiyu.db")


def query_cn_word(name=None, category=None, user=None, status=None):
    sql = "select id, name, category, status, user from cn_word where 1=1 "
    if name:
        sql += "and name like '%{}%' ".format(name)
    if category:
        sql += "and category='{}' ".format(category)
    if user:
        sql += "and user='{}' ".format(user)
    if status:
        sql += "and status='{}' ".format(status)
    sql += "order by id desc"
    return select_data(db_path, sql)


def add_cn_word(name, category, user, status):
    sql = ("insert into cn_word(name, category, user, status) "
           "values('{}',{},'{}',{})").format(name, category, user, status)
    return insert_data(db_path, sql)


def delete_cn_word(word_id):
    sql = "delete from cn_word where id={}".format(word_id)
    return delete_data(db_path, sql)


def update_cn_word(word_id, category, status):
    sql = "update cn_word set category='{}', status='{}' where id={}".format(category, status, word_id)
    return update_data(db_path, sql)

def query_random_cn_word(query_mode):
    """
    随机查询一条记录
    :param query_mode: 0-随机未学会， 1-随机所有， 2-随机已学会， 3-展示所有
    :return:
    """
    sql = "select id, name, category, status, user from cn_word where status=0 order by random() limit 1"
    if query_mode == 1:
        sql = "select id, name, category, status, user from cn_word order by random() limit 1"
    elif query_mode == 2:
        sql = "select id, name, category, status, user from cn_word where status=1 order by random() limit 1"
    elif query_mode == 3:
        sql = "select id, name, category, status, user from cn_word order by id desc"
    return select_data(db_path, sql)


def cal_cn_word():
    sql = "select count(*) from cn_word"
    all_count =  select_data(db_path, sql)
    sql = "select count(*) from cn_word where status=1"
    known_count =  select_data(db_path, sql)
    sql = "select count(*) from cn_word where status!=1"
    unknown_count =  select_data(db_path, sql)
    return all_count, known_count, unknown_count
