from xenondb.core import TYPE_MAP

LIKE_SYMBOL = "%"

def __is(data, condition):
    return data == condition

def __is_not(data, condition):
    return data != condition

def __in(data, condition):
    return data in condition

def __not_in(data, condition):
    return data not in condition

def __greater(data, condition):
    return data > condition

def __less(data, condition):
    return data < condition

def __less_and_equal(data, condition):
    return data <= condition

def __greater_and_equal(data, condition):
    return data >= condition

# 这里没有实现* 只是很单纯实现了一下%
def __like(data, condition):
    tmp = condition.split(LIKE_SYMBOL)
    length = len(tmp)
    if length == 3:
        condition = tmp[1]
    elif length == 2:
        raise Exception('Syntax Error')
    elif length == 1:
        condition = tmp[0]
    return condition in data

def __range(data, condition):
    return condition[0] <= data <= condition[1]

SYMBOL_MAP = {
    'IN':__in,
    'NOT_IN':__not_in,
    '>':__greater,
    '<':__less,
    '=':__is,
    '!=':__is_not,
    '>=':__greater_and_equal,
    '<=':__less_and_equal,
    'LIKE':__like,
    'RANGE':__range

}

class BaseCase:
    def __init__(self, condition, symbol):
        self.condition = condition
        self.symbol = symbol

    # 对新语句时，case对象重载
    def __call__(self, data, data_type):
        self.condition = TYPE_MAP[data_type.value](self.condition)
        # 如果是字符串格式 消去可能出现的引号
        if isinstance(self.condition, str):
            self.condition = self.condition.replace("'", '').replace('"', '')
        return SYMBOL_MAP[self.symbol](data, self.condition)

# 将多种case放进列表
# 例子中 比如 a is 2， 其中2是condition data_type是2：int
class BaseListCase(BaseCase):
    def __call__(self, data, data_type):
        if not isinstance(self.condition, list):
            raise TypeError('condition type error, value must be %s' % data_type)
        conditions = []
        for value in self.condition:
            value = TYPE_MAP[data_type.value](value)
            if isinstance(value, str):
                value = value.replace("'", '').replace('"', '')
            conditions.append(value)
        return SYMBOL_MAP[self.symbol](data, conditions)

class IsNotCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol='!=')

class IsCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol='=')

class InCase(BaseListCase):
    def __init__(self, condition):
        super().__init__(condition, symbol='IN')

class NotInCase(BaseListCase):
    def __init__(self, condition):
        super().__init__(condition, symbol="NOT_IN")

class GreaterCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol=">")

class LessCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol="<")

class GAECase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol=">=")

class LAECase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol="<=")

class LikeCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, symbol="LIKE")


# datatype到底是什恶魔！！！
    def __call__(self, data, data_type):
        self.condition = TYPE_MAP[data_type.value](self.condition)
        return SYMBOL_MAP[self.symbol](str(data), self.condition)

class RangeCase(BaseCase):
    def __init__(self, start, end):
        super().__init__((int(start), int(end)),symbol='RANGE')

    def __call__(self, data, data_type):
        if not isinstance(self.condition, tuple):
            raise TypeError('not a tuple condition')
        return SYMBOL_MAP[self.symbol](data, self.condition)


