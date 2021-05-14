import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        import time
        time.sleep(10)
        self.write("Hello, world")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Index")

application = tornado.web.Application([
    (r"/main", MainHandler),
    (r"/index", IndexHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# 同步形式
# http://127.0.0.1:8888/main
# http://127.0.0.1:8888/index
# main返回页面后才会返回index页面