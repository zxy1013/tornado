import socket
import base64
import hashlib

def get_headers(data):
    """
    将请求头格式化成字典
    :param data:
    :return:
    """
    header_dict = {}
    data = str(data, encoding='utf-8')

    header, body = data.split('\r\n\r\n', 1)
    header_list = header.split('\r\n')
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
        else:
            k, v = header_list[i].split(':', 1)
            header_dict[k] = v.strip()

    return header_dict


# 服务端开启socket，监听IP和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8002))
sock.listen(5)
# 等待用户连接
conn, address = sock.accept()
# 接收握手消息
data = conn.recv(8096)
headers = get_headers(data)
# print('请求头内容：')
# for k,v in headers.items():
#     print(k,':', v)
magic_string =  '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
value = headers['Sec-WebSocket-Key'] + magic_string
# 获取握手消息，magic string ，sha1并加密
ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())

# 发送回客户端
response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection:Upgrade\r\n" \
                   "Sec-WebSocket-Accept:%s\r\n" \
                   "WebSocket-Location:ws://%s%s\r\n\r\n"
response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
conn.send(bytes(response_str, encoding='utf-8'))

# 发送的规则
def send_msg(conn, msg_bytes):
    import struct
    # 发送时需要加上一个字节
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg_bytes
    conn.send(msg)
    return True


'''
    长度小于126，则只需要7位
    长度是126，则需要额外2个字节的大小，也就是 Extended payload length = info[2:4]
    长度是127，则需要额外8个字节的大小，也就是 Extended payload length + Extended payload length continued = info[2:10]，Extended payload length 是2个字节，Extended payload length continued 是6个字节
'''
# 持续监听
while True:
    info = conn.recv(8096)
    # websocket返回消息的比特规则 https://www.cnblogs.com/lsdb/p/10949766.html
    # 确定头部信息和mask-4字节以及数据的界限
    # 第二个字节的后7个bit
    payload_len = info[1] & 127
    if payload_len == 126:
        extend_payload_len = info[2:4]
        mask = info[4:8]
        decoded = info[8:]
    elif payload_len == 127:
        extend_payload_len = info[2:10]
        mask = info[10:14]
        decoded = info[14:]
    else:
        # 后面为mask和数据 用mask解密数据
        extend_payload_len = None
        mask = info[2:6]
        decoded = info[6:]

    bytes_list = bytearray()
    # 解密数据
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    body = "收到："+ body
    print(body)
    # 发送给客户端
    send_msg(conn,bytes(body,encoding='utf-8'))

# wbsk和client均run
# 控制台下输入ws.send('hello') 可以和服务器端通信