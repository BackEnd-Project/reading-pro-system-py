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

import logging
import pika
import pika.exceptions
import config
import os
import ssl

"""
RabbitMQ
"""


class RabbitMQ:
    _channel = False

    _connection = False

    _heartbeat_interval = 25

    """
       :rtype: pika.adapters.blocking_connection.BlockingChannel
    """

    def get_channel(self):
        """
        获取channel
        :return:
        """
        return self._channel

    def publish_message(self, message, exchange, routing_key=''):
        """
        发布消息
        :param message: 消息体
        :return: 执行结果
        """
        result = self._channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message
        )
        return result

    def consume_message(self, _callback, QueueName, NoAck=False):
        """
        消费消息
        :param _callback:
        :param QueueName:
        :return:
        """
        for method_frame, properties, body in self._channel.consume(QueueName, no_ack=NoAck):
            # 消息ACK，确认已经处理
            if NoAck == False:
                self.ask_message(method_frame.delivery_tag)
            _callback(body)

    def ask_message(self, tag):
        """
        消息ACK，确认已经处理
        :param tag:
        :return:
        """
        self._channel.basic_ack(tag)

    def init_connection(self):
        """
        连接到reabbitMQ
        :return:
        """

        logging.debug("Connecting to RabbitMQ [{}:{}]".format(config.rabbitmq['host'], config.rabbitmq['port']))
        credentials = pika.PlainCredentials(config.rabbitmq['user'], config.rabbitmq['pass'])

        try:
            params = pika.ConnectionParameters(
                host=config.rabbitmq['host'],
                port=config.rabbitmq['port'],
                credentials=credentials,
                socket_timeout=10,
                retry_delay=1,
                heartbeat_interval=self._heartbeat_interval,
                connection_attempts=3
            )
            # ssl 配置
            if int(config.rabbitmq['ssl']) == 1:

                params.ssl = True
                params.ssl_options = dict(
                    ssl_version=ssl.PROTOCOL_TLSv1_2,
                    ca_certs=os.path.dirname(__file__) + "/../config/ssl/cacert.pem",
                    keyfile=os.path.dirname(__file__) + "/../config/ssl/rabbit-client.key.pem",
                    certfile=os.path.dirname(__file__) + "/../config/ssl/rabbit-client.cert.pem",
                    cert_reqs=ssl.CERT_REQUIRED
                )

            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()

            logging.debug("Connecting to RabbitMQ Success")
            return True
        except pika.exceptions.ConnectionClosed as Err:
            logging.critical("Connecting to RabbitMQ Failed")
        except Exception as Err:
            logging.critical("Connecting to RabbitMQ Failed Unknow Err!")
        return False

    def init_channel(self):
        """
        定义Channel
        :return:
        """
        # 定义Channel
        self._channel = self._connection.channel(channel_number=0)

    def close_connection(self):
        """
        close Connection
        :return:
        """
        self._connection.close()

    def init_exchange(self, exchange, exchange_type='direct'):
        """
        初始化rabbitmq exchange
        :param mq:
        :param exchange:
        :param exchange_type:
        :return:
        """
        logging.info("Checking exchange [{}] [{}], Auto Declare".format(exchange, exchange_type))
        self._channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type,
            passive=False,
            durable=True
        )

    def init_queue(self, queue_name, bind_exchage=False, durable=True, routing_key=''):
        """
        定义队列
        :param queue_name:
        :param durable:
        :param bind_exchage:
        :param routing_key:
        :return:
        """
        logging.info("Checking queue [{}], Auto Declare".format(queue_name))
        self._channel.queue_declare(
            durable=durable,
            queue=queue_name)
        if bind_exchage:
            self._channel.queue_bind(exchange=bind_exchage, queue=queue_name, routing_key=routing_key)