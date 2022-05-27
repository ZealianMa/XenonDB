from xenondb.core import SerializedInterface
from xenondb.core.Table import Table

class Database(SerializedInterface):
    def __init__(self, name):
        self.__name = name
        self.__table_names = []
        self.__table_objs = {}

    def create_table(self, table_name, **options):
        if table_name in self.__table_objs:
            raise Exception('table exists')
        self.__table_names.append(table_name)
        self.__table_objs[table_name] = Table(**options)

    def drop_tables(self, table_name):
        if table_name not in self.__table_names:
            raise Exception('table not exist')
        self.__table_names.remove(table_name)
        self.__table_objs.pop(table_name, True)

    def get_table_obj(self, name):
        return self.__table_objs.get(name, None)

    def get_name(self):
        return self.__name

    def serialized(self):
        # 初始化返回数据
        data = {'name': self.__name, 'tables': []}

        for tb_name, tb_data in self.__table_objs.items():
            data['tables'].append([tb_name, tb_data.serialized()])
        return SerializedInterface.json.dumps(data)

    def add_table(self, table_name, table):
        # 如果表名不存在 开始绑定
        if table_name not in self.__table_objs:
            # 追加表明到__table_names
            self.__table_names.append(table_name)
            # 绑定对象
            self.__table_objs[table_name] = table

    @staticmethod
    def deserialize(obj):
        print(1)
        # 解析data为dict字典
        data = SerializedInterface.json.loads(obj)

        obj_tmp = Database(data['name'])
        # 遍历所有table json 依次调用table对象的反序列化方法，再添加到刚刚实例化出来的database对象中
        for table_name, table_obj in data['tables']:
            obj_tmp.add_table(table_name, Table.deserialized(table_obj))
        return obj_tmp

    def get_table(self, index = None):
        length = len(self.__table_names)
        if isinstance(index, int) and -index < length > index:
            return self.__table_names[index]
        return self.__table_names

