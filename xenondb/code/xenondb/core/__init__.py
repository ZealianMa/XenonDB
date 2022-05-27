import json
from enum import Enum

class SerializedInterface:
    # 该对象实例就不需要import
    json = json

    # 反序列化
    @staticmethod
    def deserialiized(obj):
        raise NotImplementedError


    def serialized(self):
        raise NotImplementedError


class FieldType(Enum):
    INT = int = 'int'
    VARCHAR = varchar = 'str'
    FLOAT = float = 'float'

TYPE_MAP = {
    'int': int,
    'float': float,
    'str': str,
    'INT': int,
    'FLOAT': float,
    'VARCHAR': str
}
    # 用于判断实际赋值时数据类型是否相符


# 约束
class FieldKey(Enum):
    PRIMARY = 'PRIMARY_KEY'
    INCREMENT = 'AUTO_INCREMENT'
    UNIQUE = 'UNIQUE'
    NOT_NULL = 'NOT NULL'
    NULL = 'NULL'

