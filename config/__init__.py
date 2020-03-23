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
import os
from disconf.DooDisConf import DooDisConf

# 当前API版本
api_version = 'v1'
listen = 8080

# 配置源
config_source = os.getenv('CONFIG_SOURCE', 'disconf')

# mysql 配置文件(reading_pro_system数据库)
rp_db = {
    'db': os.getenv('DB_RP_NAME', "reading_pro_system"),
    'host': os.getenv('DB_RP_HOST', "122.114.197.99"),
    'port': int(os.getenv('DB_RP_PORT', 3306)),
    'user': os.getenv('DB_RP_USER', "root"),
    'pass': os.getenv('DB_RP_PASSWORD', "XXFZsscb0316"),
    'charset': 'utf8'
}


__all__ = ['rp_db']
