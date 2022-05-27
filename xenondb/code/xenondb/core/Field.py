from xenondb.core import FieldKey, FieldType, TYPE_MAP
from xenondb.core import SerializedInterface

# 数据字段对象
class Field(SerializedInterface):
    def __init__(self, data_type, keys=FieldKey.NULL, default = None):
        # 数据类型
        self.__type = data_type
        # 数据约束
        self.__keys = keys
        # 数据默认值
        self.__default = default
        # 字段数据
        self.__values = []
        # 数据长度
        self.__rows = 0

        if not isinstance(self.__keys, list):
            # 约束只有一个时，把它设置为list
            # print("checkpoint")
            self.__keys = [self.__keys]

            # 字段类型如果不是FieldType抛出异常
        if not isinstance(self.__type, FieldType):
            raise TypeError('Data-Type require a type from "FieldType"')

        # print("checkpoint2", self.__keys, isinstance(self.__keys, list))
        for key in self.__keys:
            if not isinstance(key, FieldKey):
                raise TypeError()

        # 如果有自增约束，判断数据类型是否为整形和是否有主键约束
        if FieldKey.INCREMENT in self.__keys:
            if self.__type != FieldType.INT:
                raise TypeError('Increment key require Data-Type is integer')
            if FieldKey.PRIMARY not in self.__keys:
                raise TypeError('Increment key require primary key')

        # 如果默认值不为空并且设置了唯一约束，抛出唯一约束不能设置默认值异常
        if self.__default is not None and self.__keys == FieldKey.UNIQUE:
            raise TypeError('Unique key not allow to set default value')


#????这个value是哪来的？？
    def __check_type(self, value):
        # 如果该值类型不符合定义好的类型，则抛出类型错误答案
        # print(self.__type)
        # print(FieldType.TYPE_MAP.value[self.__type.value])
        if value is not None and not isinstance(value, TYPE_MAP[self.__type.value]):
            raise TypeError('Data type error, value must be %s' % self.__type)

        # 指定位置数据是否存在
    def __check_index(self, index):
        # 如果不存在 抛出该元素异常
        if not isinstance(index, int) or not self.__rows > index >= 0:
            raise Exception('This element not found')
        return True

    # 约束处理
    def __check_keys(self, value):
        if FieldKey.INCREMENT in self.__keys:
            # 如果字段空 则
            if value is None:
                value = self.__rows + 1
            # 如果字段重复（不满足唯一性）
            if value in self.__values:
                raise Exception('value %s exists' % value)

        # 非空查验与非重复查验
        if FieldKey.PRIMARY in self.__keys or FieldKey.UNIQUE in self.__keys:
            if value in self.__values:
                raise Exception('Value %s exist' % value)

        if FieldKey.PRIMARY in self.__keys or FieldKey.NOT_NULL in self.__keys:
            if value is None:
                raise Exception('Field Not NULL')

        return value

    # 返回数据长度
    def length(self):
        return self.__rows

    # 获取数据（查）
    def get_data(self, index=None):
        if index is not None and self.__check_index(index):
            return self.__values[index]
        return self.__values

    # 添加数据（增）
    def add(self, value):
        # 如果插入为空 插入为default
        if value is None:
            value = self.__default
        # 查询约束
        value = self.__check_keys(value)
        # 查询数据类型是否符合要求
        self.__check_type(value)
        # 添加数据
        self.__values.append(value)
        # 数据长度加一
        self.__rows += 1

    def delete(self, index):
        # 如果删除位置不存在,则抛出不存在异常
        self.__check_index(index)
        # 删除数据
        self.__values.pop(index)
        # 长度
        self.__rows -= 1

    def modify(self, index, value):
        self.__check_index(index)
        value = self.__check_keys(value)
        self.__check_type(value)
        self.__values[index] = value

    # 暴露变量
    def get_keys(self):
        return self.__keys

    def get_type(self):
        return self.__type

    def get_rows(self):
        return self.__rows


    # 序列化最后要转换为json字符串，为了符合格式，我们用枚举可以让属性在字符串和变量之间转换
    def serialized(self):
        return SerializedInterface.json.dumps({
            'key':[key.value for key in self.__keys],
            'type':self.__type.value,
            'values':self.__values,
            'default':self.__default
        })

    # 反序列化对象 把导入的json变成Field类型
    @staticmethod
    def deserialized(data):
        json_data = SerializedInterface.json.loads(data)
        keys = [FieldKey(key) for key in json_data['key']]
        # 初始化obj
        obj = Field(FieldType(json_data['type']), keys, default=json_data['default'])
        # 添加元素
        for value in json_data['values']:
            obj.add(value)
        return obj

