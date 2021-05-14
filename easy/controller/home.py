import tornado.ioloop
import tornado.web


class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        xx = self.get_secure_cookie('mmmmm')
        if not xx:
            self.redirect('/login')
            return # 必须return 否则程序会继续执行
        self.write('欢迎登陆')
