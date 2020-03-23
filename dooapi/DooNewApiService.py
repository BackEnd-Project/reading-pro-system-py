import demjson
import hashlib
import hmac
import logging
import time
import urllib3
import uuid
from urllib.parse import urlencode

# 忽略InsecureRequestWarning警告，不验SSL证书
# 参考https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
urllib3.disable_warnings()


class DooNewApiService(object):
    _encode_url_methods = ['POST', 'PUT', 'PATCH', 'DELETE']
    _time_stamp = 0
    _method = ''
    _params = ''
    _params_url_encode = ''

    def __init__(self, app_id, app_secret, app_host):
        # 检查数据
        if app_id is None:
            raise Exception('App_id Cannot Be None')
        if app_secret is None:
            raise Exception('App_secret Cannot Be None')
        if app_host is None:
            raise Exception('App_host Cannot Be None')

        self.app_id = app_id
        self.app_secret = app_secret
        self.app_host = app_host

    # 请求接口
    def call(self, api_path, method='GET', params={}):
        self._method = method.upper()
        self._params = demjson.encode(params)
        headers = self.create_headers()

        http = urllib3.PoolManager()

        # 'POST', 'PUT', 'PATCH', 'DELETE'方法请求
        if self._method in self._encode_url_methods:
            request_url = '{}{}'.format(self.app_host, api_path)
            start_time = time.time()
            response = http.request(self._method, request_url, body=self._params, headers=headers)
        # 'GET', 'HEAD', 'OPTIONS'方法请求
        else:
            request_url = '{}{}?{}'.format(self.app_host, api_path, self._params_url_encode)
            start_time = time.time()
            response = http.request(self._method, request_url, headers=headers)
        response_time = (time.time() - start_time) * 1000
        logging.info('Request URI: {}'.format(request_url))
        logging.info('Request self._params: {}'.format(self._params))
        return {
            'result': response.data.decode(),
            'status': response.status,
            'time': float('%.2f' % response_time)
        }

    # 上传文件接口
    def upload(self, api_path, params, file_path):
        # 读取bytes类型的文件
        suffix = file_path.split('.')[-1]
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # bytes类型的文件拼接到params
        file_dict = {'file_field': ('{}.{}'.format(uuid.uuid4(), suffix), file_data)}
        params.update(file_dict)

        http = urllib3.PoolManager()
        request_url = '{}{}'.format(self.app_host, api_path)
        start_time = time.time()
        response = http.request('POST', request_url, fields=params)
        response_time = (time.time() - start_time) * 1000
        logging.info('Request URI: {}'.format(request_url))
        logging.info('Request params: {}'.format(demjson.encode(params)))
        return {
            'result': response.data.decode(),
            'status': response.status,
            'time': float('%.2f' % response_time)
        }

    # 生成请求headers
    def create_headers(self):
        self._time_stamp = int(time.time())
        return {
            'Content-Type': 'application/json',
            'X-Auth-Appid': self.app_id,
            'X-Auth-Timestamp': self._time_stamp,
            'X-Auth-Nonce': str(uuid.uuid4()),
            'X-Auth-Signature': self.create_sign()
        }

    # 生成请求签名
    def create_sign(self):
        if self._method in self._encode_url_methods:
            message = '{}{}{}'.format(self._method, self._params, self._time_stamp).encode()
        else:
            # 转义原参数中空格变为'+'问题
            self._params_url_encode = urlencode(demjson.decode(self._params)).replace('+', '%20').replace('%27', '%22')
            message = '{}{}{}'.format(self._method, self._params_url_encode, self._time_stamp).encode()
        signature = hmac.new(self.app_secret.encode(), message, digestmod=hashlib.sha256).hexdigest()
        return signature


# if __name__ == '__main__':
#     app = 'appcc6113a06601'
#     secret = '01A5xFPWpyKP2aomc7vPITbEeTKMRDwb'
#     host = 'api-dev.doo.tech:18443'
#     api = '/v2/debug'
#     body = {
#         "b": "b",
#         "a": "中文",
#         "c": 100,
#         "g": [{'c': 'c'}, {'b': 1.4}],
#         "d": {"k": "v", "x": 1},
#         "e": ' ',
#         "f": [1, {"m": "中文"}, "x"]
#     }
#     service = DooNewApiService(app, secret, host)
#     result = service.call(api, 'get', body)
#     # result = service.call(api, 'get')
#     print(result['result'])
