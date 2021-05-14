import tornado.web

class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html',msg= "") # 必须传参数

    def post(self, *args, **kwargs):
        username = self.get_argument('user') # 在url或body中都可取
        password = self.get_argument('pwd')
        if username == "root" and password == '123':
            self.set_secure_cookie('mmmmm','wwwww') # 设置签名cookie
            self.redirect('/home')
        else:
            self.render('login.html',msg="用户名或密码错误")
