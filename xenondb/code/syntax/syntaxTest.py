from enm import Enum
from collections import Counter

class Foo:
    def __init__(self, ia, ib):
        self.a = ia
        self.b = ib

    def apo(self):
        return self.a + 1

    def __getitem__(self, key):
        print('__getitem__', key)

    def __setitem__(self, key):
        print('__setitem__')

    def __delitem__(self, key):
        print('__delitem__', key)



def m(f, it):
    for i in range(len(it)):
        it[i] = f(it[i])

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


@log
def now():
    print("Aa")
# 装在now上面，log返回wrapper 又返回函数本身 其实只要看wrapper里面代码就好了 wrapper里面就print了一下log传进来的函数的名字

#
#
# class Foo:
#     def run(self):
#         print(a)

if __name__ == "__main__":
    # a = 'a' % 'b'
    # print(a)

    foo = Foo(1, 2)
    print(foo.apo())
    # foo.apo(foo.a)
    m = Counter()
    m[(1, 2)] = 1

    now()

    # now = log(now)
    # now()

    foo = Foo(1, 2)
    print(Foo.__doc__)

    # a = Foo['k1']
    print(Foo.__dict__)