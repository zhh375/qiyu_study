from common.sqlite_rw import select_data, delete_data, insert_data, update_data
import os
import time
from datetime import datetime, timedelta


db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db/qiyu.db")


def query_cn_word(name=None, category=None, user=None, status=None):
    sql = "select id, name, category, status, user, update_time from cn_word where 1=1 "
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
    sql = "select id from cn_word where name='{}'".format(name)
    if select_data(db_path, sql):
        return False
    sql = ("insert into cn_word(name, category, user, status, create_time, update_time) "
           "values('{}',{},'{}',{}, {}, {})").format(name, category, user, status, int(time.time()), int(time.time()))
    return insert_data(db_path, sql)


def delete_cn_word(word_id):
    sql = "delete from cn_word where id={}".format(word_id)
    return delete_data(db_path, sql)


def update_cn_word(word_id, category, status):
    sql = ("update cn_word set category={}, status={}, update_time={} where id={}"
           .format(category, status, int(time.time()), word_id))
    return update_data(db_path, sql)

def query_random_cn_word(query_mode):
    """
    随机查询一条记录
    :param query_mode: 0-随机未学会， 1-随机所有， 2-随机已学会， 3-随机拼音
    :return:
    """
    sql = "select id, name, category, user, status, update_time from cn_word where status=0 and category!=0 order by random() limit 1"
    if query_mode == 1:
        sql = "select id, name, category, user, status, update_time from cn_word where category!=0 order by random() limit 1"
    elif query_mode == 2:
        sql = "select id, name, category, user, status, update_time from cn_word where status=1 and category!=0 order by random() limit 1"
    elif query_mode == 3:
        sql = "select id, name, category, user, status, update_time from cn_word where category=0 order by random() limit 1"
    return select_data(db_path, sql)


def cal_cn_word():
    sql = "select count(*) from cn_word"
    all_count =  select_data(db_path, sql)
    sql = "select count(*) from cn_word where status=1"
    known_count =  select_data(db_path, sql)
    sql = "select count(*) from cn_word where status!=1"
    unknown_count =  select_data(db_path, sql)

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp_start = int(today_start.timestamp())
    today_end = today_start + timedelta(days=1)
    timestamp_end = int(today_end.timestamp())
    sql = ("select count(*) from cn_word where status=1 and update_time>{} and update_time<{}"
           .format(timestamp_start, timestamp_end))
    today_count =  select_data(db_path, sql)
    return all_count, known_count, unknown_count, today_count
