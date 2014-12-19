# -*- coding: utf-8 -*-

from uuid import uuid4
from twisted.web import server, resource
from twisted.python import log
from twisted.internet import reactor, endpoints
import pika

QUEUE_HTTPLISTENER = "httplistener"
QUEUE_VALIDATION = "validation.messages"
COUNT = 1

credentials = pika.PlainCredentials('lv128', 'lv128')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)  

class HTTPListener(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        message = request.args.get("msg")
        if message and isinstance(message, list):
            message = message[0]
        log.msg(message)
        return "OK-GET"

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
        self.get_msg(QUEUE_HTTPLISTENER)
        with open("/opt/lv128/log/validation_queue.log", "a+") as validation_file:
            validation_file.write(triplet + '\n')
        log.msg(message)
        return triplet  # for debugging
        
    def send_msg(self, my_queue, my_msg):
        channel = connection.channel()
        channel.queue_declare(my_queue)
        channel.basic_publish(exchange='', routing_key=my_queue, body=str(my_msg))
        
    def callback(self, ch, method, properties, body):
        """this function consume messages and acknowledge them"""
        
        log.msg(body)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return True

    def get_msg(self, my_queue):
        channel = connection.channel()
        channel.queue_declare(my_queue)
        channel.basic_qos(prefetch_count=COUNT)
        channel.basic_consume(self.callback, queue=my_queue)
        return body
            
log.startLogging(open('/opt/lv128/log/HTTPListener.log', 'w'))
endpoints.serverFromString(reactor, "tcp:8812").listen(server.Site(HTTPListener()))
reactor.run()

