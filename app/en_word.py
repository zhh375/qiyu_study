from common.sqlite_rw import select_data, delete_data, insert_data, update_data
import os
import time
from datetime import datetime, timedelta


db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db/qiyu.db")


def query_en_word(name=None, category=None, user=None, name_type=None, status=None, parent_id=None):
    sql = "select id, name, category, status, user, type, update_time from en_word where 1=1 "
    if name:
        sql += "and name like '%{}%' ".format(name)
    if category:
        sql += "and category='{}' ".format(category)
    if user:
        sql += "and user='{}' ".format(user)
    if status:
        sql += "and status='{}' ".format(status)
    if name_type:
        sql += "and type='{}' ".format(name_type)
    if parent_id:
        sql += "and parent_id='{}' ".format(parent_id)
    sql += "order by id desc"
    return select_data(db_path, sql)


def add_en_word(name, category, user, name_type, status):
    sql = (("insert into en_word(name, category, user, type, status, create_time, update_time) "
           "values('{}',{},'{}',{}, {}, {}, {})")
           .format(name, category, user, status, name_type, int(time.time()), int(time.time())))
    return insert_data(db_path, sql)


def delete_en_word(word_id):
    sql = "delete from en_word where id={}".format(word_id)
    return delete_data(db_path, sql)


def update_en_word(word_id, category, status):
    sql = ("update en_word set category={}, status={}, update_time={} where id={}"
           .format(category, status, int(time.time()), word_id))
    return update_data(db_path, sql)

def query_random_en_word(query_mode, category=0):
    """
    随机查询一条记录
    :param category: 类别1-其它，2-牛津树，3-海尼曼，4-英语启蒙Olga
    :param query_mode: 0-随机未学会单词， 1-随机所有单词， 2-随机已学会单词， 3-随机未学会句子， 4-随机所有句子， 5随机已学会句子， 6-随机字母
    :return:
    """
    sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
           "where status=0 and type=0 and category={category} order by random() limit 1".format(category=category))
    if query_mode == 1:
        sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
               "where type=0 and category={category} order by random() limit 1".format(category=category))
    elif query_mode == 2:
        sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
               "where status=1 and type=0 and category={category} order by random() limit 1".format(category=category))
    elif query_mode == 3:
        sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
               "where status=0 and type=1 and category={category} order by random() limit 1".format(category=category))
    elif query_mode == 4:
        sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
               "where type=1 and category={category} order by random() limit 1".format(category=category))
    elif query_mode == 5:
        sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
               "where status=1 and type=1 and category={category} order by random() limit 1".format(category=category))
    elif query_mode == 6:
        sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
               "where type=2 and category={category} order by random() limit 1".format(category=category))

    return select_data(db_path, sql)


def query_random_en_word_parent_id(parent_id):
    """
    随机查询一条记录
    :param parent_id:
    :return:
    """
    sql = ("select id, name, category, user, type, status, parent_id, update_time from en_word "
           "where parent_id={} order by random() limit 1").format(parent_id)
    return select_data(db_path, sql)


def cal_en_word():
    sql = "select count(*) from en_word where type=0"
    all_count_word =  select_data(db_path, sql)
    sql = "select count(*) from en_word where type=1"
    all_count_some_word =  select_data(db_path, sql)
    sql = "select count(*) from en_word where status=1 and type=0"
    known_count_word =  select_data(db_path, sql)
    sql = "select count(*) from en_word where status=1 and type=0"
    known_count_some_word =  select_data(db_path, sql)
    sql = "select count(*) from en_word where status!=1"
    unknown_count =  select_data(db_path, sql)

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp_start = int(today_start.timestamp())
    today_end = today_start + timedelta(days=1)
    timestamp_end = int(today_end.timestamp())
    sql = ("select count(*) from en_word where status=1 and update_time>{} and update_time<{}"
           .format(timestamp_start, timestamp_end))
    today_count =  select_data(db_path, sql)
    return all_count_word, all_count_some_word, known_count_word, known_count_some_word, unknown_count, today_count
