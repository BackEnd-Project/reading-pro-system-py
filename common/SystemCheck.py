"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2018 DooHolding Inc. (http://www.doo.tech)
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

import config
from playhouse.pool import PooledMySQLDatabase


class SystemCheck:
    @staticmethod
    def check():

        try:
            # 使用连接池
            database = PooledMySQLDatabase(database=config.rp_db['db'], max_connections=300,
                                           **{
                                               'host': config.rp_db['host'],
                                               'port': int(config.rp_db['port']),
                                               'user': config.rp_db['user'],
                                               'passwd': config.rp_db['pass'],
                                               'charset': 'utf8'})
            database.connect()
            database.close()
        except Exception as Err:
            print('***** reading_pro_db database error')
            return False
        print("***** reading_pro_db database ok")
        return True
