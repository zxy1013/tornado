import tornado.web
import tornado.ioloop
import tornado.websocket

# HTTP请求
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


users = set()
# WebSocket请求继承tornado.websocket.WebSocketHandler
class ChatHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        """
        客户端和服务端已经建立连接 tornado建立的 打开http://127.0.0.1:8888/自动执行
        1. 连接
        2. 握手
        """
        print(self.__dict__.get('ui').get('modules'))
        print('来人了')
        users.add(self)

    # 前端sendMessage()发消息 后台收消息message
    def on_message(self, message):
        print(message)
        # 模板引擎渲染字符串
        content = self.render_string('message.html',msg=message)
        for client in users:
            client.write_message(content) # 发送给前端  每个人都接收

    def on_close(self):
        """
        客户端主动关闭连接时执行
        """
        print(self.__dict__.get('ui').get('modules'))
        print('跑了一个人')
        users.remove(self)


def run():
    settings = {
        'template_path': 'templates',
        'static_path': 'static',
    }
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# http://127.0.0.1:8888/
# 可开多个窗口

if __name__ == "__main__":
    run()