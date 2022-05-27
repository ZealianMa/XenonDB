# class Foo:
#     def __init__(self):
#         self.a = 1
#         self.b = [1,2,3]
#
#     def __setitem__(self, key, value):
#         self.__dict__[key] = value
#         print("set", key, value)
#
#     def __iter__(self):
#         return iter(self.b)
#
#
# a = Foo()
# print(a.__dict__)
# a['c'] = 3
# print(a.__dict__)
#
# # for i in map(int,input().split()):
#     # print(i)
#
# for i in a:
#     print(i)
#
#
# def foo():
#     print("start")
#     a = 0
#     while 1:
#         yield a
#         a += 1
#
# # foo不会被真正的执行 赋值时先得到生成器g
# print(foo())
# g = foo()
# # 调用next方法 foo开始真正执行 先print start 然后进入循环
# print(next(g))
# print("*" * 20)
# print(next(g))
#
# for i in range(10):
#     print(next(g))
#     # print("*(*")
#
#
# # 一个可以不用生成列表的方法
# def boo(num):
#     print("starting..")
#     while num < 10:
#         num += 1
#         yield num
#
# for n in boo(0):
#     print(n)
#
# a = boo(1)
# print(next(a))
#
# print(isinstance(3, int))
#
# print(int)
#
# for obj in range(10):
#     print(obj)

from collections import Counter
n = int(input())
cnt = Counter()
ll = list(map(int,input().split()))
ans = 0
for i in ll:
    cnt[i] += 1
for i in ll:
    if cnt[i] == 1:
        ans += i
print(ans)