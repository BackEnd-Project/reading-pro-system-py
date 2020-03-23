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

import common, json, logging, uuid, hashlib, hmac, urllib3, certifi, config
from binascii import b2a_hex

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where(),
    maxsize=10,
    retries=1,
    timeout=6
)

class DooApi():

    appid = None
    appsecret = None
    gateway = None
    version = 'v1'
    caching = False
    connection = http

    def __init__(self, appid, appsecret, gateway=config.api_gateway):
        """
        构造方法
        :param appid:
        :param appsecret:
        :param version:
        :param gateway:
        """
        self.appid = appid
        self.appsecret = appsecret
        self.gateway = gateway

    def set_connection_pool(self, pool):
        self.connection = pool

    def set_caching(self, caching):
        """
        设置是否缓存
        :param caching:
        :return:
        """
        self.caching = caching

    def set_version(self, version):
        """
        设置api版本号
        :param version:
        :return:
        """
        self.version = version

    def set_gateway(self, gateway):
        """
        设置api网关
        :param gateway:
        :return:
        """
        self.gateway = gateway

    def create_sign(self, sign_str):
        """
        创建签名
        @see https://document.doohui.com/confluence/pages/viewpage.action?pageId=50462739
        :param params:
        :return:
        """
        sign = hmac.new(self.appsecret.encode(), sign_str.encode(), hashlib.sha256).digest()
        return b2a_hex(sign)

    def build_headers(self, method, params):
        """
        构造请求参数
        @see https://document.doohui.com/confluence/pages/viewpage.action?pageId=50462734
        :param method:
        :param params:
        :return:
        """
        req_timestamp = str(int(common.getUnixTime()))

        header = {
            'X-Auth-Appid': self.appid,
            'X-Auth-Nonce': str(uuid.uuid4()),
            'X-Auth-Timestamp': req_timestamp,
            'X-Auth-Signature': ''
        }
        request_params = self.pack_request_sign_params(method, params)
        sign_str = "{}{}{}".format(method, request_params, req_timestamp)
        header['X-Auth-Signature'] = self.create_sign(sign_str)
        return header

    def pack_request_sign_params(self, method, params):
        """
        构造请求数据字符串
        :param params:
        :return:
        """
        # GET
        if method == 'GET':
            if params == None:
                return ""
            tmp = ""
            for key in params:
                tmp += "{}={}&".format(key, params[key])
            return tmp[:len(tmp) - 1]
        # POST etc.
        return json.dumps(params)

    def call(self, method, api, path, body = None):
        """
        :return:
        """
        result = None

        if self.version == '':
            # 兼容服务无版本号的情况
            api = "{}{}/{}".format(self.gateway, api, path)
        else:
            if api == '':
                api = "{}{}{}/{}".format(self.gateway, api, self.version, path)
            else:
                api = "{}{}/{}/{}".format(self.gateway, api, self.version, path)
        headers = self.build_headers(method, body)

        logging.info("request api: {}".format(api))
        logging.info("headers: ")
        logging.info(headers)

        try:

            # GET
            if method == 'GET':
                response = self.connection.request(method, api, headers = headers, fields=body)

            # POST | DELETE | PUT
            if method == 'POST' or method == 'DELETE' or method == 'PUT':
                body = json.dumps(body)
                response = self.connection.request(method, api, body = body, headers = headers)

            result = response.data

        except urllib3.exceptions.MaxRetryError:
            return {
                'code': -1,
                'data': {
                    'info': 'API_ERROR_{}'.format("TIMEOUT")
                }
            }

        try:
            result_json = json.loads(result.decode('utf-8'))
            # 临时的网关错误数据补充
            if 'code' not in result_json and 'message' in result_json:
                result_json = {
                    'code': -1,
                    'data': 'API ERROR {}'.format(result_json['message'])
                }
        except ValueError as Err:
            logging.critical("Json Decode Err: {}\n{}".format(result, Err))
            return None

        return result_json