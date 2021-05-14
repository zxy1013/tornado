# -*-coding:utf-8-*-
# @ Auth:zhao xy
# @ Time:2021/5/11 19:32
# @ File:app.py

import tornado.ioloop
import tornado.web
from easy.controller.account import LoginHandler
from easy.controller.home import HomeHandler
import easy.ext.uimethods as mt
import easy.ext.uimodules as mm

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world") # 返回字符串
        # self.render("main.html") # 渲染模板
        # self._headers # 拿到请求头
        # self.request.files['name'] # 取文件
        self.redirect('http://www.baidu.com')


settings = {
    "template_path": 'template',
    'cookie_secret':'dhjfstyiohzdawuohfgsrthxfs', # cookie加密密钥
    'ui_methods': mt, # 注册自定制模块
    'ui_modules': mm,
    'static_path': 'static',
    # 'autoescape':None, # 设置UIMethod不自动转义
}

# 设置view和url路径匹配
application = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/login", LoginHandler),
    (r"/home", HomeHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8888) # 监听8888端口
    tornado.ioloop.IOLoop.instance().start()
    # run
    # http://127.0.0.1:8888/index
    # http://127.0.0.1:8888/login