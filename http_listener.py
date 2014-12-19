# -*- coding: utf-8 -*-

from uuid import uuid4
from twisted.web import server, resource
from twisted.python import log
from twisted.internet import reactor, endpoints
import pika

QUEUE_HTTPLISTENER = "httplistener"
QUEUE_VALIDATION = "validation.messages"
COUNT = 1

credentials = pika.PlainCredentials('guest', 'guest')
#credentials = pika.PlainCredentials('lv128', 'lv128')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
#connection = pika.BlockingConnection(parameters)

class HTTPListener(resource.Resource):
    isLeaf = True

    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        message = request.args.get("msg")
        if message and isinstance(message, list):
            message = message[0]
        log.msg(message)

        body = self.get_msg(QUEUE_HTTPLISTENER)
        return body

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        message = request.args.get("msg", "")
        token = request.args.get("token", "")
        if message and isinstance(message, list):
            message = message[0]
        if token and isinstance(token, list):
            token = token[0]
        triplet = ':'.join([uuid4().hex, token, message])
        self.send_msg(QUEUE_VALIDATION, triplet)
        body = self.get_msg(QUEUE_HTTPLISTENER)
        with open("/opt/lv128/log/validation_queue.log", "a+") as validation_file:
            validation_file.write(triplet + '\n')
        log.msg(message)
        return body

    def send_msg(self, my_queue, my_msg):
        self.channel.queue_declare(my_queue)
        self.channel.basic_publish(exchange='', routing_key=my_queue, body=str(my_msg))

    def callback(self, ch, method, properties, body):
        """this function consume messages and acknowledge them"""

        log.msg(body)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return True

    def get_msg(self, my_queue):
        """The function takes message from the queue"""

        self.channel.queue_declare(my_queue)
        for method_frame, properties, body in self.channel.consume(my_queue):
            print body
            self.log.info(CONNECT_ON)
            self.log.info(body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return body

    def _get_msg(self, my_queue):
        self.channel.queue_declare(my_queue)
        self.channel.basic_qos(prefetch_count=COUNT)
        self.channel.basic_consume(self.callback, queue=my_queue)

log.startLogging(open('HTTPListener.log', 'w'))
endpoints.serverFromString(reactor, "tcp:8812").listen(server.Site(HTTPListener()))
reactor.run()

