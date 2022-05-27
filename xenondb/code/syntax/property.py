class foo:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        # 设置为私有变量 无法在外部直接访问

    def get_age(self):
        return self.__age

    def get_name(self):
        return self.__name

    def set_age(self, newage):
        if isinstance(newage, int):
            self.__age = newage
        else:
            raise ValueError

    def del_age(self):
        print('del')

    age = property(get_age, set_age, del_age, "年龄")
    name = property(get_name)

a = foo("X", 18)
print(a.age)
a.age = 20
print(a.age)
del a.age
print(a.age)

# a = foo("X", 18)
# print(a.get_age(), a.get_name())
# a.set_age(20)
# print(a.get_age())

# class foo:
#     def __init__(self, name, age):
#         self.__name = name
#         self.__age = age
#         # 设置为私有变量 无法在外部直接访问
#
#     @property
#     def age(self):
#         return self.__age
#
#     @property
#     def name(self):
#         return self.__name
#
#     @age.setter
#     def age(self, value):
#         if isinstance(value, int):
#             self.__age = value
#         else:
#             raise ValueError('非整数类型')
#
#     @age.deleter
#     def age(self):
#         print('del')


# a = foo("X", 18)
# print(a.age, a.name)
# a.age = 20
# print(a.age)
# del a.age
# print(a.age)

class Foo:
    def __init__(self,a):
        self.a = a
    @staticmethod
    def aa(c):
        print(c * 10)

a = Foo.aa(10)
# a.aa(3)