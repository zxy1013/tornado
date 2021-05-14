import socket
import select

# 自定义同步web框架
# 不为异步非阻塞
import time


class HttpRequest(object):
    """
    封装用户请求信息
    """
    def __init__(self, content):
        """
        content:用户发送的请求数据：请求头和请求体
        """
        self.content = content
        self.header_bytes = bytes()
        self.body_bytes = bytes()
        self.header_dict = {}
        self.method = ""
        self.url = ""
        self.protocol = ""
        self.initialize() # 分请求头和请求体
        self.initialize_headers() # 处理请求头

    def initialize(self):
        temp = self.content.split(b'\r\n\r\n', 1)
        if len(temp) == 1:
            self.header_bytes += temp
        else:
            h, b = temp
            self.header_bytes += h
            self.body_bytes += b

    @property # 返回请求头
    def header_str(self):
        return str(self.header_bytes, encoding='utf-8')

    def initialize_headers(self):
        headers = self.header_str.split('\r\n')
        first_line = headers[0].split(' ')
        if len(first_line) == 3:
            self.method, self.url, self.protocol = headers[0].split(' ')
            for line in headers:
                kv = line.split(':')
                if len(kv) == 2:
                    k, v = kv
                    self.header_dict[k] = v


def main(request):
    time.sleep(5)
    return "main"

def index(request):
    return "*************************"


# 路由
routers = [
    ('/main',main),
    ('/index',index),
]

def run():
    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 9999,))
    sock.setblocking(False)
    sock.listen(128)

    inputs = []
    inputs.append(sock)
    while True:
        # io多路复用 最大超时时间0.05
        rlist,wlist,elist = select.select(inputs,[],[],0.05)
        for r in rlist:
            if r == sock:
                # 新请求到来
                conn,addr = sock.accept()
                # 客户端不阻塞
                conn.setblocking(False)
                inputs.append(conn)
            else:
                # 客户端发来数据
                data = b"" # 字节
                # 一次可能接收不完
                while True:
                    try:
                        chunk = r.recv(1024) # 接收完成后会报错
                        data = data + chunk
                    except Exception as e:
                        chunk = None
                    if not chunk:
                        break # 接收完成

                # 对data进行处理：请求头和请求体
                request = HttpRequest(data)
                # print(request.url)
                # print(request.header_dict)

                # 1. 请求头中获取url
                # 2. 去路由中匹配，获取指定的函数
                # 3. 执行函数，获取返回值
                # 4. 将返回值 r.sendall('****')
                import re
                flag = False
                func = None
                for route in routers: # [0] url [1] 函数  # 匹配函数和url
                    if re.match(route[0],request.url):
                        flag = True
                        func = route[1]
                        break
                if flag:
                    result = func(request) # 执行url匹配的函数
                    r.sendall(bytes(result,encoding='utf-8'))
                else: # 未匹配成功
                    r.sendall(b"404")

                inputs.remove(r) # http是短连接，接收完成后关闭 请求一次 响应一次后结束
                r.close()

if __name__ == '__main__':
    run()

# http://127.0.0.1:9999/main
# http://127.0.0.1:9999/index
# index页面等待main页面返回再返回