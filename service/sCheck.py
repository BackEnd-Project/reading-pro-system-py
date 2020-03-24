
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
# import config


resource = dir()


class sCheck:

    def check(self):
        """
        检查配置环境
        :return:
        """
        data_dicts = {}
        for item in resource:
            if item.find("rp_db") >= 0:
                try:
                    common.get_mysql(item)
                    data_dicts["rp_db_check"] = "ok"
                except Exception as Err:
                    data_dicts["rp_db_check"] = "down"
                    data_dicts["rp_db_check_error"] = str(Err)

        keys_list = list(data_dicts.keys())
        for key in keys_list:
            if key.find("error") >= 0:
                data_dicts[key[0:-6]] = "down"
        return data_dicts

