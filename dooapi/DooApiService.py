"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
"""

import logging
import demjson
import urllib3
import hashlib
import time
import uuid
from service.DooSecure import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DooApiService():

    Appid = ''
    AppSecret = ''
    AppHost = ''

    def __init__(self, Appid, AppSecret, AppHost):

        # 对数据类型进行检查
        if Appid is None:
            raise Exception('Appid Cannot Be None')
        if AppSecret is None:
            raise Exception('AppSecret Cannot Be None')
        if AppHost is None:
            raise Exception('AppHost Cannot Be None')

        self.Appid = Appid
        self.AppSecret = AppSecret
        self.AppHost = AppHost

    def call_api(self, path, params, isPost = False):
        """
        请求接口
        :param path:
        :param params:
        :param isPost:
        :return:
        """
        http = urllib3.PoolManager()
        RequestURI = '{}{}'.format(self.AppHost, path)
        RequestParams = self.build_params(params)
        # GET
        if not isPost:
            # RequestURI = RequestURI + '?c='+ RequestParams['c'] + '&d=' + RequestParams['d'] + '&t=' \
            #              + str(RequestParams['t']) + '&s=' + RequestParams['s'] + '&r=' + RequestParams['r']
            startTime = time.time()  # 请求接口前时间
            Result = http.request('GET', RequestURI)
        # POST
        else:
            startTime = time.time()  # 请求接口前时间
            Result = http.request('POST', RequestURI, fields=RequestParams)
        ResponseTime = (time.time() - startTime) * 1000
        ResponseTime = float('%.2f' % ResponseTime)
        return {
            'result': Result.data,
            'status_code': Result.status,
            'time': ResponseTime
        }

    # 请求接口
    def call(self, path, params, isPost = False):
        http = urllib3.PoolManager()
        RequestURI = '{}{}'.format(self.AppHost, path)
        RequestParams = self.build_params(params)
        # GET
        if not isPost:
            # RequestURI = RequestURI + '?c='+ RequestParams['c'] + '&d=' + RequestParams['d'] + '&t=' \
            #              + str(RequestParams['t']) + '&s=' + RequestParams['s'] + '&r=' + RequestParams['r']
            startTime = time.time()  # 请求接口前时间
            Result = http.request('GET', RequestURI)
        # POST
        else:
            startTime = time.time()  # 请求接口前时间
            Result = http.request('POST', RequestURI, fields=RequestParams)
        ResponseTime = (time.time() - startTime) * 1000
        ResponseTime = float('%.2f' % ResponseTime)
        Result = Result.data
        Result = Result.decode(encoding='utf-8')
        return Result, ResponseTime

    # 上传文件接口
    def upload(self, path, params, fileParams):
        http = urllib3.PoolManager()
        RequestURI = '{}{}'.format(self.AppHost, path)
        RequestParams = self.build_params(params)
        RequestParams = dict(RequestParams)
        RequestParams.update(fileParams)
        startTime = time.time()  # 请求接口前时间
        Result = http.request('POST', RequestURI, fields=RequestParams)
        logging.info("Request URI {}".format(RequestURI))
        logging.info("Request Params {}".format(RequestParams))
        ResponseTime = (time.time() - startTime) * 1000
        ResponseTime = float('%.2f' % ResponseTime)
        Result = Result.data
        Result = Result.decode(encoding='utf-8')

        return Result, ResponseTime

    def build_params(self, RequestData):
        _params = {}
        _params['c'] = self.Appid
        _params['d'] = self.encrypt_data(RequestData)
        _params['t'] = int(time.time())
        _params['r'] = str(uuid.uuid4())
        _params['s'] = self.create_sign(_params)
        return _params

    # 加密数据
    def encrypt_data(self, RequestData):
        Secure = DooSecure(self.AppSecret)
        RequestDataJson = demjson.encode(RequestData)
        return Secure.encrypt_base64(RequestDataJson)

    # 创建签名
    def create_sign(self, _params):
        SignStr =  'c={}&d={}&r={}&t={}&key={}~dsha1'.format(_params['c'], _params['d'], _params['r'], _params['t'], self.AppSecret)
        SignStr = hashlib.sha1(SignStr.encode(encoding='utf-8'))
        return SignStr.hexdigest()