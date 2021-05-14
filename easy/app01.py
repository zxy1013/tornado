# -*-coding:utf-8-*-
# @ Auth:zhao xy
# @ Time:2021/5/12 15:01
# @ File:app01.py

import tornado.ioloop
import tornado.web


# # 单继承
# class Foo(tornado.web.RequestHandler):
#     def initialize(self): # 将源码中的initialize改写
#         self.A = 123
#         super(Foo,self).initialize() # 将源码中的initialize继承
#
# class MainHandler(Foo):
#     def get(self):
#         print(self.A)
#         self.write("Hello, world")


# 多继承
class Foo(object):
    def initialize(self): # 写方法initialize
        self.A = 123

class MainHandler(Foo,tornado.web.RequestHandler): # 继承Foo的方法initialize
    def get(self):
        print(self.A)
        self.write("Hello, world")


application = tornado.web.Application([
    (r"/index", MainHandler),
])

# run
# http://127.0.0.1:9999/index

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()