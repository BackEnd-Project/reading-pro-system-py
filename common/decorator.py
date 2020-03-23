import config
from classes.RabbitMQ import RabbitMQ
import error
import exceptions
import peewee
import logging
import json
from common import DateTimeEncoder


def audit_publish_task(self, data):
    """
    结算单审核发布队列
    :param self:
    :param data:
    :return:
    """
    if self.mq is None:
        logging.info("{} is None, prepare to init".format(self.mq))
        self.mq = RabbitMQ()
        self.mq.init_connection()
    self.mq.publish_message(json.dumps(data, cls=DateTimeEncoder), config.auto_audit_exchange)
    self.mq.close_connection()


def audit_validate_publish_decorator(val_func):
    def validate_data(func):
        """
        数据校验与结算单审核队列发布装饰器
        :param func:
        :return:
        """

        def _wrapper(self, param):
            try:
                val_func(self.arguments)
                result = func(self, param)
                if result:
                    audit_publish_task(self, result)
            except error.RequestData as e:
                self.echo_error(e.code, e.message)
            except exceptions.Database as e:
                self.echoJson(e.code, e.message)
            except peewee.DoesNotExist:
                self.echoJson()
            except Exception as e:
                self.echoJson(exceptions.exception, str(e))

        return _wrapper

    return validate_data
