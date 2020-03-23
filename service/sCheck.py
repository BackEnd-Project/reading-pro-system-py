
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

import common
from config import *
import config


resource = dir()

class sCheck:

    def check(self):
        """
        获取事件主表列表
        :param page:
        :param pagesize:
        :param search:
        :return:
        """
        data_dicts = {}
        print(resource)
        for item in resource:

            if item.find("elastic_social") >= 0:
                try:
                    es = common.get_es_social()
                    if es.ping():
                        data_dicts["elastic_social_check"] = "ok"
                except Exception as Err:
                    data_dicts["elastic_social_check"] = "down"
                    data_dicts["elastic_social_check_error"] = str(Err)

            if item.find("elastic_mt") >= 0:
                try:
                    es = common.get_es_social()
                    if es.ping():
                        data_dicts["elastic_mt_check"] = "ok"
                except Exception as Err:
                    data_dicts["elastic_mt_check"] = "down"
                    data_dicts["elastic_mt_check_error"] = str(Err)

            if item.find("social_sp_db") >= 0:
                try:
                    common.get_mysql(item)
                    data_dicts["social_sp_db_check"] = "ok"
                except Exception as Err:
                    data_dicts["social_sp_db_check"] = "down"
                    data_dicts["social_sp_db_check_error"] = str(Err)

            if item.find("follow_db") >= 0:
                try:
                    common.get_mysql(item)
                    data_dicts["follow_db_check"] = "ok"
                except Exception as Err:
                    data_dicts["follow_db_check"] = "down"
                    data_dicts["follow_db_check_error"] = str(Err)

            if item.find("mt_db") >= 0:
                try:
                    common.get_mysql(item)
                    data_dicts["mt_db_check"] = "ok"
                except Exception as Err:
                    data_dicts["mt_db_check"] = "down"
                    data_dicts["mt_db_check_error"] = str(Err)

            if item.find("social_user_db") >= 0:
                try:
                    common.get_mysql(item)
                    data_dicts["social_user_db_check"] = "ok"
                except Exception as Err:
                    data_dicts["social_user_db_check"] = "down"
                    data_dicts["social_user_db_check_error"] = str(Err)

            if item == "rabbitmq":
                try:
                    print("mq host: {} port: {} user: {} ssl: {}".format(config.rabbitmq['host'], config.rabbitmq['port'], config.rabbitmq['user'], config.rabbitmq['ssl']))
                    common.get_rabbitmq()
                    data_dicts["rabbitmq_check"] = "ok"
                except Exception as Err:
                    data_dicts["rabbitmq_check"] = "down"
                    data_dicts["rabbitmq_check_error"] = str(Err)
        keys_list = list(data_dicts.keys())
        for key in keys_list:
            if key.find("error") >= 0:
                data_dicts[key[0:-6]] = "down"
        return data_dicts

