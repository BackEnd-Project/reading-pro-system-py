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
                     ..
               .`         `.:/:`      `-/+ooo
           `-/+oo/    `.:/ooooo-  `.:+ooooooo
       `.:+oooooo/ `-/+ooo++ooo- :oooo+/-+ooo
   `.:/oooo+/:ooo/ .ooo+:.`:ooo- /ooo-`  +ooo
  `:+ooooo.` `ooo/ .ooo:   :ooo- /ooo.   +ooo
    `.oooo   `ooo/ .ooo:   :ooo- /ooo.   +ooo
      +ooo   `ooo/ .ooo:   :ooo- /ooo.   +ooo
      +ooo   `ooo/ .ooo:   :ooo- /ooo.   +ooo
      +ooo   `ooo/ .ooo:   :ooo- /ooo. `.+ooo
      +ooo   .ooo/ .ooo:`.:+ooo- /ooo:/+oooo/
      +ooo-/+oooo: .ooo++ooo+/-` /oooooo+:-`
     `+oooooo+/-`  .ooooo/:.`    :oo+/-``   `
  `-/+oooo/-`      `://-`         `.`    `:/+
   .:/+:.`                                .:/
"""

import urllib3
import certifi
import hashlib
import json
import uuid
import os


class DooDisConf:
    # 服务器地址
    host = os.getenv('DISCONF_HOST', 'http://192.168.1.203:12888/')

    # 配置项密钥
    conf_secret = os.getenv('DCONF_SECRET', 'RrlLN0dQxnHTzSjf4ybPEK7MOF8t')

    @staticmethod
    def get(key):
        """
        获取配置文件
        :param key:
        :return:
        """
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
            maxsize=1
        )
        params = dict(
            key=key,
            nonstr=uuid.uuid4().__str__()
        )
        request_params = DooDisConf.pack_data(params)
        response = http.request('GET', DooDisConf.host + 'conf/get/{}'.format(request_params))
        result = response.data
        return json.loads(result.decode())['data']

    @staticmethod
    def hash_md5(raw_str):
        """
        hash('md5') 加密
        :param raw_str:
        :return:
        """
        if raw_str is None or raw_str == "":
            return raw_str
        hl = hashlib.md5()
        hl.update(raw_str.encode(encoding='utf-8'))
        return hl.hexdigest()

    @staticmethod
    def pack_data(params) -> str:
        """
        打包参数
        :param params:
        :return:
        """
        _r = ''
        # 签名
        params['sign'] = DooDisConf.hash_md5('{}{}{}'.format(params['key'], params['nonstr'], DooDisConf.conf_secret))
        for k in params:
            _r += '{}={}&'.format(k, params[k])
        return '?' + _r[:-1]
