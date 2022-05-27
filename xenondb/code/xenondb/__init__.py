from xenondb.core.Database import Database
from xenondb.core import SerializedInterface
from xenondb.parser import SQLParser
import os
import base64
import prettyTables

# 解妈
def _decode_db(content):
    content = base64.decodebytes(content)
    return content.decode()[::-1]

# 编码
def _encode_db(content):
    content = content[::-1].encode()
    return base64.encodebytes(content)

class Engine:
    def __init__(self, db_name = None, format_type = 'dict', path = 'db_data'):
        # 数据库映射表
        self.__database_objs = {}
        # 数据库名
        self.__database_names = []
        # 状态绑定 标记当前使用的数据库
        self.__current_db = None

        self.__format = format_type
        # 如果初始化时数据库名字不为空，调用select_db方法选中数据库(此时数据库选中为db_name)
        if db_name is not None:
            self.select_db(db_name)

    # 这里有一个问题 如何初始化engine？？？？
    #     昨天刚问今天就来方法了
        self.path = path

        self.__load_databases()

        self.__action_map = {
            'insert': self.__insert,
            'update': self.__update,
            'search': self.__search,
            'delete': self.__delete,
            'drop': self.__drop,
            'show': self.__show,
            'use': self.__use,
            'exit': self.__exit
        }


    def run(self):
        while 1:
            statement = input('\033[00;37xenondb> ')
            try:
                ret = self.execute(statement)
                if ret in ['exit', 'quit']:
                    print("bye")
                    return
                if ret:
                    pt = prettyTables.PrettyTable(ret[0].keys())
                    pt.align = 'l'
                    for line in ret:
                        pt.align = 'r'
                        pt.add_row(line.values())
                    print(pt)
            except Exception as exc:
                print('\033p00;31m' + str(exc))

    def __insert(self, action):
        table = action['table']
        data = action['data']
        return self.insert(table, data = data)

    # def __select(self, action):
    #     table = action['table']
    #     fields = action['fields']

        # return self.insert(table, data = data)

    def __update(self, action):
        table = action['table']
        data = action['data']
        conditions = action['conditions']
        return self.update(table, data = data, conditions = conditions)

    def __delete(self, action):
        table = action['table']
        conditions = action['conditions']
        return self.update(table, conditions = conditions)

    def __search(self, action):
        table = action['table']
        fields = action['fields']
        conditions = action['conditions']
        return self.search(table, fields = fields, conditions = conditions)

    def __drop(self, action):
        if action['kind'] == 'database':
            return self.drop_database(action['name'])
        return self.drop_table(action['name'])

    def __show(self, action):
        if action['kind'] == 'databases':
            return self.get_databases(format_type='dict')
        return self.get_table(format_type='dict')

    def __use(self, action):
        return self.select_db(action['database'])

    def __exit(self, _):
        return 'exit'

    def execute(self, statement):
        action = SQLParser().parse(statement)
        ret = None
        if action['type'] in self.__action_map:
            ret = self.__action_map.get(action['type'])(action)
            if action['type'] in ['insert', 'update', 'delete', 'create', 'drop']:
                self.commit()
        return ret

    def create_database(self, database_name):
        if database_name in self.__database_objs:
            raise Exception('Database exist')
        # 追加数据库名字
        self.__database_names.append(database_name)
        # 关联数据库
        self.__database_objs[database_name] = Database(database_name)

    def drop_database(self, database_name):
        # 如果数据库名字不存在 则抛出数据库不存在异常
        if database_name not in self.__database_objs:
            raise Exception('Database % is not exits' % database_name)
        # 用列表 remove方法移除
        self.__database_names.remove(database_name)
        # 移除数据库名和对象映射
        self.__database_objs.pop(database_name, True)

    def select_db(self, db_name):
        if db_name not in self.__database_objs:
            raise Exception('has not this database')
        # 讲对应名字的database对象赋值给__current_db
        self.__current_db = self.__database_objs[db_name]
        print(self.__current_db)

    # 序列化
    def serialized(self):
        return SerializedInterface.json.dumps([
            database.serialized() for database in self.__database_objs.values()
        ])

    def deserialized(self, content):
        # 解析
        data = SerializedInterface.json.loads(content)
        # print(len(data))
        # 因为每一条是一个db对象的json数据 所以直接遍历再调用db的反序列化方法就行了
        for obj in data:
            database = Database.deserialize(obj)
            # 获取数据库名字
            db_name = database.get_name()
            # 追加数据库名字和绑定数据库对象
            self.__database_names.append(db_name)
            self.__database_objs[db_name] = database

    def __dump_databases(self):
        with open(self.path, 'wb') as f:
            # 编码json
            content = _encode_db(self.serialized())
            # 保存数据到本地
            f.write(content)

    # 加载数据库
    def __load_databases(self):
        # 如果数据文件不存在 则直接退出
        if not os.path.exists(self.path):
            return
        # 读取文件数据
        with open(self.path, 'rb') as f:
            content = f.read()
        # 如果数据不为空
        if content:
            self.deserialized(_decode_db(content))

    def commit(self):
        self.__dump_databases()

    def rollback(self):
        self.__load_databases()

    def search(self, table_name, fields = "*", sort = 'ASC', **conditions):
        return self.__get_table(table_name).search(fields = fields, sort = sort, format_type = self.__format)

    def __get_table(self, table_name):
        # 判断当前是否有选中的数据库
        self.__check_is_choose()
        # 获取对应table对象
        table = self.__current_db.get_table_obj(table_name)
        if table is None:
            raise Exception('table %s is not found' % table_name)
        return table

    def __check_is_choose(self):
        if not self.__current_db or not isinstance(self.__current_db, Database):
            raise Exception('No database choose')

    def insert(self, table_name, **data):
        return self.__get_table(table_name).insert(**data)

    def update(self, table_name, data, **conditions):
        self.__get_table(table_name).update(data, **conditions)

    def delete(self, table_name, **conditions):
        return self.__get_table(table_name).delete(**conditions)

    def create_table(self, name, **options):
        self.__check_is_choose()
        self.__current_db.create_table(name, **options)

    def get_databases(self, format_type='list'):
        databases = self.__database_names
        if format_type == 'dict':
            tmp = []
            for database in databases:
                tmp.append({'name':databases})
            databases = tmp
        return databases

    # 获取数据表
    def __get_table(self, table_name):
        self.__check_is_choose()
        table = self.__current_db.get_table_obj(table_name)
        if table is None:
            raise Exception('not table %s' % table_name)
        return table

    # 获取数据表名字
    def get_table(self, format_type = "list"):
        self.__check_is_choose()
        tables = self.__current_db.get_table()
        if format_type == "dict":
            tmp = []
            for table in tables:
                tmp.append({'name':table})
            tables = tmp
        return tables
