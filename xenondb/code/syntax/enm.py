from math import sqrt
# from enum import Enum
#
# class Foo:
#     def __init__(self):
#         a = 1
#
#
# class Color(Enum):
#     red = 1
#     green = 2
#     blue = 3
#     TYPE = {
#         red : 'red',
#         green : 'green',
#         blue : 'blue',
#     }
#
# print(Color.red.name)
# print(Color.red.value)
# for color in Color:
#     print(color)
#
# INT = int = 'int'
# print(INT)
# # print(Color.NULL)
# # print(red.value)
# a = 1
# # print(isinstance(Color[Color.red.value], Color))
# foo = Foo()
# foo.value

a = list(map(int,input().split()))
b = list(map(int,input().split()))
print([i^2 for i in a])
aa = sqrt(sum([i*i for i in a]))
bb = sqrt(sum([i*i for i in b]))
s = 0
print(aa, bb)
for i in range(len(a)):
    s += a[i] * b[i]
print(s)
print(s / (aa * bb))