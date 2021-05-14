import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.concurrent import Future
import time

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        # 特殊的形式等待5s 5s后处理self.done
        future = Future()
        tornado.ioloop.IOLoop.current().add_timeout(time.time() + 5, self.done)
        yield future # 监听返回的future里的result有没有值 如果没有，监听就不断开
        # 5s后值返回了 检测到有值，执行done函数断开连接

    def done(self, *args, **kwargs):
        self.write('Main')
        self.finish()

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

# 异步非阻塞
# http://127.0.0.1:8888/main
# http://127.0.0.1:8888/index
# index不等待main返回页面