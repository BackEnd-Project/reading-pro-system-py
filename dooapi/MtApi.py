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

from dooapi.DooApi import DooApi

class MtApi(DooApi):
    api = 'mt'

    version = 'v1'

    def get_mt_server(self, appid):
        """
        获取mt服务器列表 hash
        :param page:
        :param search:
        :return:
        """
        result = self.call('GET', self.api, 'server/', {
            'appid': appid,
            'server_type': 'mt4',
            'type': 'social'
        })
        return result

    def get_group(self, server_id):
        """
        获取mt服务器列表 hash
        :param page:
        :param search:
        :return:
        """
        result = self.call('GET', self.api, 'account/group/info', {
            'server_id': server_id
        })
        return result
