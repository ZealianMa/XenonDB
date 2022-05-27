# def func(nums):
#     while nums < 10:
#         yield nums
#         nums += 1
#
# def fun(nums):
#     return nums
#
# if __name__ == "__main__":
#     a = func(0)
#     for i in a:
#         print(i)
#
#
#
#     # print(a)
#     # for i in a:
#     #     pass
#
#
#
#     ml = [i**2 for i in range(10)]
#     mg = (i**2 for i in range(2, 10))
#     print(ml, mg)
#     print(next(mg))
#     print(next(mg))
#     for ele in mg:
#         print(ele)
#     print(mg)
#     print(ml.__iter__)
#     iter_ml = ml.__iter__()
#     print(ml.__iter__().__next__())
#     print(ml.__iter__().__next__())
#     print(ml.__iter__().__next__())
#     print(iter_ml.__next__())
#     print(iter_ml.__next__())
#     print(iter_ml.__next__())
#
#
#     print("*********")
#     iter_ml = ml.__iter__()
#     while 1:
#         try:
#             print(iter_ml.__next__())
#         except StopIteration:
#             print("迭代完了")
#             break
# #
# #
# #
# print((4*0.49 + 5*0.4)/0.56)

class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, c, d):
        return (self.a + c) - (self.b + d)

class Boo(Foo):
    def __init__(self, e):
        super(Boo, self).__init__(1, e)

class Boo2(Foo):
    def __init__(self, e):
        self.e = e
        # print(self.e + self.a)

class Ns(Foo):
    def __call__(self, c, d):
        return self.a + c - (self.b + d)



if __name__ == "__main__":
    print("checkpoint")
    a = Boo(3)
    print(a(2, 4))
    print(isinstance(a, Foo), isinstance(a, Boo))
    b = Ns(2, 1)
    print(b(3, 2))
    print(isinstance(b, Foo))
    print("checkpoint")
    boo2 = Boo2(3)
    print(isinstance(boo2, Foo))
