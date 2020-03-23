"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
"""

import tornado.httpclient
from .BaseHandler import BaseHandler
import exceptions
import peewee
import error
import validate
from service.sUser import sUser
from common.decorator import audit_validate_publish_decorator
from tornado import gen
import common


class UserHandler(BaseHandler):
    """
    User（用户）
    :return:
    """

    service = sUser()

    @tornado.web.asynchronous
    def get(self, uid):
        """
        获取用户列表信息
        :param uid:
        :return object:
        """
        del self.arguments['appid']
        try:
            # validate.billing_get(self.arguments)
            if uid is not None and uid is not '':
                self.arguments['uid'] = uid
                result = self.service.get_info(**self.arguments)
                self.echoJson(0, result)
            else:
                # 如果没有 id 的话 就是获取列表
                result, counts = self.service.get_list(**self.arguments)
                self.echoJson(0, {"data": result, "totalCounts": counts})
        except error.RequestData as e:
            self.echo_error(e.code, e.message)
        except exceptions.RequestData as e:
            self.echoJson(e.code, e.message)
        except peewee.DoesNotExist:
            self.echoJson()
        except Exception as e:
            self.echoJson(exceptions.exception, str(e))
        self.close_connect_and_finish()

    @tornado.web.asynchronous
    def post(self, param):
        """
        创建用户
        :param param:
        :return object:
        """
        try:
            # validate.billing_get(self.arguments)

            result = self.service.create_user(**self.arguments)
            self.echoJson(0, {"info": result.uid})
        except error.RequestData as e:
            self.echo_error(e.code, e.message)
        except exceptions.RequestData as e:
            self.echoJson(e.code, e.message)
        except peewee.DoesNotExist:
            self.echoJson()
        except Exception as e:
            self.echoJson(exceptions.exception, str(e))
        self.close_connect_and_finish()
