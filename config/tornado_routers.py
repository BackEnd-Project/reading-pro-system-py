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

import handler
from config import api_version

uuid_pattern = "?(\w*-*\w*-*\w*-*\w*-*\w*)"

# 请求路由
routers = [
    # check
    (r"/{}/check/{}".format(api_version, uuid_pattern), handler.CheckHandler),
    # 用户
    (r"/{}/user/{}".format(api_version, uuid_pattern), handler.UserHandler),
]
