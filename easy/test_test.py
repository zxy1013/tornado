# -*-coding:utf-8-*-
# @ Auth:zhao xy
# @ Time:2021/5/12 14:43
# @ File:test_test.py

class C:
	def f1(self):
		print('C')
		super(C, self).f1( )  # 执行B的方法

class A(C):
	def f1(self): # 重写C的f1方法
		# print(self) # self永远是调用方法的对象 Foo <__main__.Foo object at 0x000001C76E078B08>
		print('A')
		super(A,self).f1() # 执行C的方法
		# super().f1( )  # 同上，执行C的方法
		B.f1(self) # 执行B的方法

class B:
	def f1(self):
		# print(self) # <__main__.Foo object at 0x00000238B56A8AC8>
		print('B')

class Foo(A, B):
	pass

obj = Foo() # super里的列表 按这个顺序执行super调用[A,C,B]   A-->C-->B  最后打印B
obj.f1()



# # **in对象 自动调用__contains__方法
# class Foo:
# 	def __contains__(self, item):
# 		print(item)
# 		return True
#
# obj = Foo()
# v = "x" in obj # **in对象 自动调用__contains__方法