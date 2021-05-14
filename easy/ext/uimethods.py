from tornado import escape

def tab(request,val):
    # 会自动传递请求相关信息 request
    return '<h1>hello world</h1>'