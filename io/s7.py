import socket
import select

# 异步非阻塞web框架
import time


class HttpRequest(object):
    """
    用户封装用户请求信息
    """
    def __init__(self, content):
        self.content = content
        self.header_bytes = bytes()
        self.body_bytes = bytes()
        self.header_dict = {}
        self.method = ""
        self.url = ""
        self.protocol = ""
        self.initialize()
        self.initialize_headers()

    def initialize(self):
        temp = self.content.split(b'\r\n\r\n', 1)
        if len(temp) == 1:
            self.header_bytes += temp
        else:
            h, b = temp
            self.header_bytes += h
            self.body_bytes += b

    @property
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


class Future(object):
    def __init__(self, timeout=0):
        self.result = None
        self.timeout = timeout # 超时时间
        self.start = time.time( ) # 创建future对象的时间

F = None
def main(request):
    global F
    F = Future(5)
    return F

def index(request):
    return "llllllllllllllll"


# 路由
routers = [
    ('/main',main),
    ('/index',index),
]

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 9999,))
    sock.setblocking(False)
    sock.listen(128)
    inputs = []
    inputs.append(sock)
    async_request_dict = { # 存储挂起的程序
    }
    while True:
        rlist,wlist,elist = select.select(inputs,[],[],0.05)
        for r in rlist:
            if r == sock:
                """新请求到来"""
                conn,addr = sock.accept()
                conn.setblocking(False)
                inputs.append(conn)
            else:
                """客户端发来数据"""
                data = b""
                while True:
                    try:
                        chunk = r.recv(1024)
                        data = data + chunk
                    except Exception as e:
                        chunk = None
                    if not chunk:
                        break
                # 对data进行处理：请求头和请求体
                request = HttpRequest(data)
                # 1. 请求头中获取url
                # 2. 去路由中匹配，获取指定的函数
                # 3. 执行函数，获取返回值
                # 4. 将返回值 r.sendall(b'alskdjalksdjf;asfd')
                import re
                flag = False
                func = None
                for route in routers:
                    if re.match(route[0],request.url):
                        flag = True
                        func = route[1]
                        break
                if flag:
                    result = func(request)
                    if isinstance(result,Future): # main函数阻塞
                        async_request_dict[r] = result
                    else:
                        r.sendall(bytes(result,encoding='utf-8'))
                        inputs.remove(r)
                        r.close()
                else:
                    r.sendall(b"404")
                    inputs.remove(r)
                    r.close()

        # 循环挂起的程序，关闭连接
        for conn in list(async_request_dict.keys()):
            future = async_request_dict[ conn ]
            start = future.start # 创建对象的时间
            timeout = future.timeout # 超时时间
            ctime = time.time( )
            if (start + timeout) <= ctime:
                future.result = b"timeout" # 设置值
            if future.result:
                conn.sendall(future.result)
                conn.close( )
                del async_request_dict[conn] # 删除挂起的对象
                inputs.remove(conn) # 删除连接

if __name__ == '__main__':
    run()

# http://127.0.0.1:9999/main
# http://127.0.0.1:9999/index