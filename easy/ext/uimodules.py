from tornado.web import UIModule
from tornado import escape

class Custom(UIModule):
    def css_files(self):
        return "commons.css" # 在head中引入静态文件
    def embedded_css(self): # 在head中嵌入css
        return ".c1{display:none}"
    def javascript_files(self): # 在body的最下面引入js文件/static/commons.js
        return "commons.js"
    def embedded_javascript(self): # 引入js代码
        return "function f1(){alert(123);}"
    def render(self, val): # 前端可以看见的函数
        # return "hello"
        # return '<h1>hello</h1>' # 本身就不会自动转义 前端显示h1标签的hello
        v = escape.xhtml_escape('<h1>hello</h1>') # 手动转义 前端显示字符串'<h1>hello</h1>'
        return v