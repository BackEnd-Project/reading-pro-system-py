"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
"""

from .BaseHandler import BaseHandler
from service.sCheck import sCheck


class CheckHandler(BaseHandler):
    service = sCheck()

    def get(self, xxx):
        """
        Check接口
        :param xxx:
        :return:
        """

        data_list = self.service.check()
        self.echoJson(0, data_list)
        self.close_connect_and_finish()
