import tornado.ioloop
import tornado.web
import socket

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname('0.0.0.0')
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.current().start()
