import tornado.ioloop
import tornado.web
from tornado import gen

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        from tornado import httpclient
        http = httpclient.AsyncHTTPClient() # 收到结果 执行self.done
        yield http.fetch("http://www.google.com", self.done)

    def done(self, *args, **kwargs):
        self.write('Main')
        self.finish() # 断开连接

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


# http://127.0.0.1:8888/main
# http://127.0.0.1:8888/index
# index页面不等待main返回页面