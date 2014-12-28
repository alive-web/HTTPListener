# -*- coding: utf-8 -*-

from uuid import uuid4
from twisted.web import server, resource
from twisted.python import log
from twisted.internet import reactor, endpoints
import pika

QUEUE_HTTPLISTENER = "httplistener"
QUEUE_VALIDATION = "validation.messages"
COUNT = 1


class HTTPListener(resource.Resource):
    isLeaf = True

    def __init__(self):
        credentials = pika.PlainCredentials('lv128', 'lv128')
        parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
        except:
            raise

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        message = request.args.get("msg")
        if message and isinstance(message, list):
            message = message[0]
        log.msg(message)
        return "OK-GET"

    def render_POST(self, request):
    	"""
    	The function listens to POST-request from client and return valid message
    	"""
        request.setHeader("content-type", "text/plain")
        message = request.args.get("msg", "")
        token = request.args.get("token", "")
        if message and isinstance(message, list):
            message = message[0]
        if token and isinstance(token, list):
            token = token[0]
        triplet = ':'.join([uuid4().hex, token, message])
        self.send_msg(QUEUE_VALIDATION, triplet)
        with open("/opt/lv128/log/validation_queue.log", "a+") as validation_file:
            validation_file.write(triplet + '\n')
        log.msg(message)
        resp = self.get_msg(QUEUE_HTTPLISTENER)
        log.msg(resp)
        if resp:
            code, msg = resp.split('|')
            request.setResponseCode(int(code))
            return msg

    def send_msg(self, my_queue, my_msg):
    	"""
    	The function declares a queue and send message there
    	"""
        self.channel.queue_declare(my_queue)
        self.channel.basic_publish(exchange='', routing_key=my_queue, body=str(my_msg))

    def get_msg(self, my_queue):
        """
        The function takes message from the queue
        """
        self.channel.basic_qos(prefetch_count=COUNT)
        try:
            for method_frame, properties, body in self.channel.consume(my_queue):
                self.channel.basic_ack(method_frame.delivery_tag)
                return body
        except pika.exceptions, err_msg:
            log.error(err_msg)
            return False


log.startLogging(open('/opt/lv128/log/HTTPListener.log', 'w'))
endpoints.serverFromString(reactor, "tcp:8812").listen(server.Site(HTTPListener()))
reactor.run()