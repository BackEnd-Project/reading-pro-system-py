"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
 *
 * May you do good and not evil
 * May you find forgiveness for yourself and forgive others
 * May you share freely, never taking more than you give.  -- SQLite source code
 *
 * As we enjoy great advantages from the inventions of others, we should be glad
 * of an opportunity to serve others by an invention of ours, and this we should
 * do freely and generously.  -- Ben Franklin
 *
 *     (\
 *     (  \  /(o)\     caw!
 *     (   \/  ()/ /)
 *      (   `;.))'".)
 *       `(/////.-'
 *    =====))=))===()
 *      ///'
 *     //
 *    '
"""

import time
import datetime
from elasticsearch import Elasticsearch
import config
import uuid
import demjson
import certifi
import hashlib
import logging
from config import *
from classes.RabbitMQ import RabbitMQ
from playhouse.pool import PooledMySQLDatabase
import json
from datetime import date


# ES的基础配置项
elastic_params = dict(
    retry_on_timeout=True,
    maxsize=200,
    timeout=5,
    verify_certs=True,
    ca_certs=certifi.where())


def getDate():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def datetime_to_string(dt):
    if str(type(dt)) == "<class 'datetime.datetime'>":
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return dt


def get_week():
    """
    获取当前星期
    :return:
    """
    week = datetime.datetime.utcnow().weekday()
    return week


def get_real_page(page_from_request):
    """
    获取数据库中真实页码，前端传的页码从1开始，所以需减1
    :param page_from_request:
    :return:
    """
    if isNumber(page_from_request) is False:
        return 0
    page_from_request = int(page_from_request)
    if page_from_request >= 1:
        return page_from_request - 1
    return page_from_request


def get_time_now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def toJson(code=0, data=None):
    Json = {
        'code': code,
        'data': data
    }
    return Json


def isNumber(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def is_json(myjson):
    """
    判断字符串是否是json字符串
    :param myjson:
    :return:
    """
    try:
        demjson.decode(myjson)
    except ValueError:
        return False
    except TypeError:
        return False
    except Exception:
        return False
    return True


def get_index_analysis(AppID, ServerID):
    """
    获取索引
    :param AppID:
    :param ServerID:
    :return:
    """
    return "{}_{}_{}".format(config.elastic_index_prefix_analysis_users, AppID, ServerID)


def getIndexTrades(AppID, ServerID):
    """
    获取索引
    :param AppID:
    :param ServerID:
    :return:
    """
    return "{}_{}_{}".format(config.elastic_index_prefix_trades, AppID, ServerID)


def get_index_mt_users(appid, server_id):
    """
    获取mt4或mt5 user索引
    :param appid:
    :param server_id:
    :return:
    """
    return "{}_{}_{}".format(config.elastic_index_prefix_users, appid, server_id)


def getIndexBalance(AppID, ServerID):
    """
    获取索引
    :param AppID:
    :param ServerID:
    :return:
    """
    return "{}_{}_{}".format(config.elastic_index_mt4_balance_analysis, AppID, ServerID)


def get_index_social_user(appid, document_type):
    """
    获取social_user的index，这里每个document_type一个独立的index
    :param appid: 经纪商的appid
    :param document_type:
    :return:
    """
    return "{}_{}_{}".format(config.elastic_index_prefix_social_user, appid, document_type)


def get_public_index_social_user(document_type):
    """
    获取指定document_type的social_user的所有公开的经纪商的alias
    :param appid: 经纪商的appid
    :param document_type:
    :return:
    """
    return "{}_{}_{}_{}".format("alias", config.elastic_index_prefix_social_user, "*", document_type)


def get_index_social_user_alias(appid, document_type):
    """
    获取指定document_type的social_user的所有公开的经纪商的alias
    :return:
    """
    return "{}_{}_{}_{}".format("alias", config.elastic_index_prefix_social_user, appid, document_type)


def get_index_analysis_alias(appid, server_id):
    """
    获取公有的分析数据的索引
    :return:
    """
    return "{}_{}_{}_{}".format("alias", config.elastic_index_prefix_analysis_users, appid, server_id)


def get_index_social_user_unique(document_type):
    """
    获取social_user的index，这里每个document_type一个独立的index
    :param document_type:
    :return:
    """
    return "{}_*_{}".format(config.elastic_index_prefix_social_user, document_type)


def create_uuid():
    """
    生成uuid
    :return: uuid
    """
    uuid = generateGID()
    hash3 = hashlib.md5(bytes(uuid[0:3], encoding='utf-8'))
    hash3.update(bytes(uuid, encoding='utf-8'))
    return (hash3.hexdigest())[0:4] + '-' + (hash3.hexdigest())[5:14]


def generateGID():
    """
    生成随机id
    :return: id
    """
    return str(uuid.uuid1()).replace("-", "")


def create_login_id():
    """
    生成随机login_id
    :return:
    """
    uuid = generateGID()
    hash3 = hashlib.md5(bytes(uuid[-3:], encoding='utf-8'))
    hash3.update(bytes(uuid, encoding='utf-8'))
    return (hash3.hexdigest())[0:4] + (hash3.hexdigest())[-4:]


def data_unique(data_list):
    """
    数据根据account去重
    :param data_list:
    :return:
    """
    if len(data_list) == 0:
        return []
    temp_list = list(set([str(i) for i in data_list]))
    li = [eval(i) for i in temp_list]
    return li


def sort_list_by_key(list_arg, key, sort="asc"):
    """
    根据key来排序列表
    :param list_arg:如 [{"a":1, "b":1},{"a":0, "b":1},{"a":2, "b":1},{"a":6, "b":1}]
    :param key: 如"a"
    :return:
    """
    if list_arg is None or len(list_arg) == 0:
        return list_arg
    try:
        if sort == "desc":
            return sorted(list_arg, key=lambda x: x[key], reverse=True)
        else:
            return sorted(list_arg, key=lambda x: x[key], reverse=False)
    except Exception as e:
        return []


def get_rabbitmq():
    mq = RabbitMQ()
    mq.init_connection()
    mq.init_channel()
    mq.close_connection()


def get_mysql(mysql1):
    mysql2 = eval(mysql1)
    database = PooledMySQLDatabase(database=mysql2['db'], max_connections=300, **{
        'host': mysql2['host'],
        'port': int(mysql2['port']),
        'user': mysql2['user'],
        'passwd': mysql2['pass'],
        'charset': 'utf8'})
    database.connect()
    database.close()


def fields_to_model(fields, _model) -> list:
    """
    根据字符串获取到模型并返回
    :param fields:
    :param _model:
    :return:
    """
    _models = []
    if fields is None:
        return []
    fields = fields.split(',')
    for f in fields:
        # 去掉空格
        f = f.strip(' ')
        if hasattr(_model, f):
            _models.append(getattr(_model, f))
    return _models


def get_elastic(_config=None) -> Elasticsearch or False:
    """
    获取ElasticSearch连接
    :return:
    """
    if _config is None:
        return None
    address = "{}:{}@{}:{}".format(
        _config['user'],
        _config['pass'],
        _config['host'],
        _config['port']
    )
    try:
        is_https = _config['method'] == 'https'
        elastic = Elasticsearch(hosts=address, use_ssl=is_https, **elastic_params)
        return elastic
    except Exception as Err:
        logging.critical(Err)
        return False


def get_es_mt():
    """
    获取ElasticSearch连接
    :return:
    """
    return get_elastic(config.elastic_mt)


def get_es_social():
    """
    获取ElasticSearch连接
    :return:
    """
    return get_elastic(config.elastic_social)


def getUnixTime():
    return int(time.time())


def generate_id():
    """
    生成随机唯一id
    :return: unique_id
    """
    char_id = str(uuid.uuid1()).replace("-", "")
    unique_id = char_id[0:4] + '-' + char_id[6:15]
    return unique_id


class DateTimeEncoder(json.JSONEncoder):
    """
    json序列化类
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


__all__ = ['get_mysql', 'toJson', 'getDate', 'getIndexTrades', 'getIndexBalance', 'create_uuid', 'generateGID']
