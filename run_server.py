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

import tornado.web, tornado.ioloop, os, logging, config, error, sys
from config.tornado_routers import routers
from tornado.options import define
from common.SystemCheck import SystemCheck

app_path = sys.path[0]
define("app_path", default=app_path)

if os.getenv('DOO_ENV', 'dev') == 'pro':
    log_level = logging.WARNING

if os.getenv('DOO_ENV', 'dev') == 'dev':
    log_level = logging.INFO

if os.getenv('DOO_ENV', 'dev') == 'debug':
    log_level = logging.DEBUG

logging.basicConfig(level=log_level,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.getLogger('elasticsearch').setLevel(logging.WARNING)

logging.getLogger('apscheduler').setLevel(logging.WARNING)

logging.getLogger('pika').setLevel(logging.WARNING)

application = tornado.web.Application(routers)

if __name__ == "__main__":

    # 系统测试
    check = SystemCheck()
    if check.check() is False:
        os._exit(-1)

    try:
        port = config.listen
        logging.info("Running on {}".format(port))
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except error.RequestData as e:
        print(e.code)
        print(e.message)