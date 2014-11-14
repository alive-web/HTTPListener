from uuid import uuid4
from twisted.web import server, resource
from twisted.python import log
from twisted.internet import reactor, endpoints

class HTTPListener(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
         request.setHeader("content-type", "text/plain")
         message = request.args.get("msg")
         if message and isinstance(message, list):
             message = message[0]
         log.msg(message)
         return "OK"

    def render_POST(self, request):
         request.setHeader("content-type", "text/plain")
         message = request.args.get("msg", "")
         token = request.args.get("token", "")
         if message and isinstance(message, list):
             message = message[0]
         if token and isinstance(token, list):
             token = token[0]
         triplet = ':'.join([uuid4().hex, token, message])

         with open("/opt/lv128/HTTPListener/validation_queue.log", "a+") as validation_file:
             validation_file.write(triplet + '\n')

         log.msg(message)
         return "OK"


log.startLogging(open('/opt/lv128/HTTPListener/requests.log', 'w'))
endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(HTTPListener()))
reactor.run()
