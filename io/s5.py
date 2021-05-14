import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.concurrent import Future

# 手写future
future = None
class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        global future
        future = Future()
        future.add_done_callback(self.done)
        yield future # 阻塞 挂起当前请求 线程处理其他请求

    def done(self, *args, **kwargs):
        self.write('Main')
        self.finish()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        global future
        future.set_result(None) # 设置future的值 当前请求以及挂起请求 均被返回
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
# index页面点击后main页面同时也被返回