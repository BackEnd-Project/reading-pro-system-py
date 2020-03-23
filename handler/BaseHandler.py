"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
"""

import tornado.web
import logging
import tornado.web
import demjson
import json
import storage.model as model


class BaseHandler(tornado.web.RequestHandler):

    DooSecure = None

    def initialize(self):
        """
        重写框架方法
        :return:
        """
        # 这里必须初始化为空，避免连接缓存
        self.arguments = {}
        # 在body中的json数据
        request_json = self.request.body.decode('utf-8')
        request_dict = {}
        if request_json is not None and request_json is not "":
            request_dict = json.loads(request_json)
        # 获取在请求url中的数据
        for key in self.request.arguments.keys():
            self.arguments[key] = bytes.decode(self.request.arguments[key][0])

        # 结合两者数据，在url中的数据优先级高
        for key in request_dict.keys():
            if self.arguments.get(key) is None:
                self.arguments[key] = request_dict[key]

        if 'appid' not in self.arguments:
            # 添加AppID, 避免覆盖参数中的appid，修改后果自负！
            self.arguments['appid'] = self.request.headers.get("X-Auth-Appid")

    def getPostData(self):
        """
        获取全部post数据
        :return:
        """
        try:
            request = self.request.body.decode('utf-8')
            requestJson = demjson.decode(request)
            # 添加AppID
            requestJson['appid'] = self.request.headers.get("X-Auth-Appid")
            return requestJson
        except Exception as Err:
            logging.critical(Err)
            return {}

    def echoJson(self, code=0, data=None):
        """
        输出Json内容
        :param arr:
        :return:
        """
        Json = {
            'code': code,
            'data': data
        }
        self.set_header("Content-Type", "application/json")
        self.write(demjson.encode(Json))

    def echoSuccess(self):
        self.echoJson(code=0, data='success')

    def echoFail(self):
        self.echoJson(code=-1, data='fail')

    def echo_error(self, error_code=20000, error_message="error"):
        """
        输出错误信息
        :param arr:
        :return:
        """
        json = {
            'code': error_code,
            'data': {"info": error_message}
        }
        self.write(demjson.encode(json))

    def close_connect_and_finish(self):
        self.finish()
        model.database.close()

