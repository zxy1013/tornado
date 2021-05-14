# -*-coding:utf-8-*-
# @ Auth:zhao xy
# @ Time:2021/5/12 15:11
# @ File:app02.py

# session组件:
# 1.生成随机字符串
# 2.写入用户cookie
# 3.后台存储
# 因为需要通过self.session['key']取值
# 一共有两种方法：字典、类的__setitem__

import tornado.ioloop
import tornado.web
import time
import hashlib


# 将session保存在内存
class Cache(object):
	# 初始化容器
	def __init__(self):
		self.container = {}
	# **in对象 调用
	def __contains__(self, item):
		return item in self.container
	# 初始化某个session_id 的k和v
	def initial(self,random_str):
		self.container[random_str] = {}
	# 取session
	def get(self,random_str,key):
		return self.container[random_str].get(key)
	# 设置session
	def set(self,random_str,key,value):
		self.container[random_str][key] = value
	# 删除session
	def delete(self,random_str,key):
		del self.container[random_str][key]
	# 打开连接
	def open(self):
		pass
	# 关闭连接
	def close(self):
		pass
	# 清除session
	def clear(self,random_str):
		del self.container[random_str]

P = Cache() # 可以设置为setting文件

class Session(object):
	def __init__(self,handler):
		self.handler = handler # **Handler的self
		self.random_str = None
		self.db = P
		self.db.open()

	# 生成随机字符串session_id
	def create_random_str(self,key):
		v = str(key)
		m = hashlib.md5()
		m.update(bytes(v,encoding='utf-8'))
		return m.hexdigest()

	# 写入内存
	def __setitem__(self, key, value):
		# 用户请求信息中获取session_id，如果没有表示为新用户
		self.db.open( )
		client_random_str = self.handler.get_cookie('session_id')
		if not client_random_str:  # "新用户"
			self.random_str = self.create_random_str(key)
			self.db.initial(self.random_str)  # 初始化该session_id的k和v
		else:
			if client_random_str in self.db: # 调用__contains__方法 判断session_id是否合法
				self.random_str = client_random_str
			else: # "非法用户"
				self.random_str = self.create_random_str(key)
				self.db.initial(self.random_str) # 初始化某个session的k和v

		# 更新登录状态 写入cookie
		ctime = time.time()
		self.handler.set_cookie('session_id',self.random_str,expires=ctime+20)
		# session：key，value
		self.db.set(self.random_str,key,value)
		self.db.close()

	# 获取
	def __getitem__(self, key):
		client_random_str = self.handler.get_cookie('session_id')
		if client_random_str in self.db:  # 调用__contains__方法 判断session_id是否合法
			self.random_str = client_random_str
			self.db.open()
			v = self.db.get(self.random_str,key)
			self.db.close()
			ctime = time.time( )
			self.handler.set_cookie('session_id', self.random_str, expires=ctime + 20)
			return v
		else:
			return None

	# 删除
	def __delitem__(self, key):
		self.db.open()
		self.db.delete(self.random_str,key)
		self.db.close()

	# 清空
	def clear(self):
		self.db.open()
		self.db.clear(self.random_str)
		self.db.close()

class Foo(object):
	def initialize(self):
		# self是**Handler对象
		# if self.__dict__.get('uri')=='/login':
		self.session = Session(self)
		super(Foo,self).initialize()

class HomeHandler(Foo,tornado.web.RequestHandler):
	def get(self):
		user = self.session['uu']
		# print(user)
		if not user:
			self.write('未登录')
		else:
			self.write(user)

class LoginHandler(Foo,tornado.web.RequestHandler):
	def get(self):
		self.session['uu'] = 'root'
		self.redirect('/home')


application = tornado.web.Application([
	(r"/login", LoginHandler),
	(r"/home", HomeHandler),
])

if __name__ == "__main__":
	application.listen(7777)
	tornado.ioloop.IOLoop.instance().start()

# run
# http://127.0.0.1:7777/login