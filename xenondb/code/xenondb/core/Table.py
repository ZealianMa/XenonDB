from xenondb.core import SerializedInterface
from xenondb.core.Field import Field
from xenondb.case import BaseCase
# 数据表：数据字段名，字段名与字段对象Field的映射，数据表大小
class Table(SerializedInterface):
# options值期望：变量名：被定义好的Field对象
    def __init__(self, **options):
        self.__field_names = []
        self.__field_objs = {}
        self.__rows = 0

        # 获取所有字段名和字段对象为数据表初始化字段
        for field_name, field_obj in options.items():
            self.add_field(field_name, field_obj)

    def add_field(self, field_name, field_obj, value=None):
        # 如果字段已经存在，避免重复添加
        if field_name in self.__field_names:
               raise Exception('Field Exists')

        # 如果obj不是Field对象，抛出异常
        if not isinstance(field_obj, Field):
            raise TypeError('error')

        # 字段名添加
        self.__field_names.append(field_name)

        # 绑定字段名和字段
        self.__field_objs[field_name] = field_obj

        # 如果已存在其他字段，同步该新增字段的数据长度
        if len(self.__field_names) > 1:
            # 获取已存在的字段长度
            length = self.__rows
            # 获取该新增字段的长度
            field_obj_length = field_obj.length()
            # 如果新增字段自身包含数据 则判断长度是否与已存在字段的长度相等
            if field_obj_length :
                if field_obj_length == length:
                    return
                raise Exception('Field data length inconformity')


            # 本身就不存在数据的情况
            # 如果不包含数据 循环初始化新增字段数据 一直到新增字段的数据长度和self.__rows相等
            for index in range(length):
                if value:
                    self.__get_field(field_name).add(value)
                else:
                    self.__get_field(field_name).add(None)
        # 这是数据表第一个字段
        else:
            # 初始化表格所有数据长度
            self.__rows = field_obj.length()

    def search(self, fields, sort, format_type, **conditions):
        # 如果*返回全部字段
        if fields == "*":
            fields = self.__field_names
        else:
            for field in fields:
                if field not in self.__field_names:
                    raise Exception('%s field not exists' % field)

        rows = []
        # 解析条件,返回列数
        match_index = self.__parse_conditions(**conditions)
        print(match_index)
        for index in match_index:
            # 返回list类型的数据 也就是没有字段名
            if format_type == 'list':
                row = [self.__get_field_data(field_name, index) for field_name in fields]
            elif format_type == 'dict':
                row = dict()
                for field_name in fields:
                    row[field_name] = self.__get_field_data(field_name, index)
            else:
                raise Exception('format type invalid')
            rows.append(row)

        if sort == "DESC":
            rows = rows[::-1]
        return rows

    def __get_field(self, field_name):
        if field_name not in self.__field_names:
            raise Exception('%s field is not exists' % field_name)
        # 这里返回的是一个__field_objs对象
        return self.__field_objs[field_name]

    def __get_field_data(self, field_name, index = None):
        field = self.__get_field(field_name)
        return field.get_data(index)

    def __get_field_type(self, field_name):
        field = self.__get_field(field_name)
        return field.get_type()


    # 条件解析
    # 如果条件是空，索引所有 反之匹配条件的索引
    # 判断字段的合理性
    # 先给字段get一下field内容 get提一下type
    # 猜测conditions变量是（key：[condition, symbol]）里面是一个basecase类！！

    # 有个挺有意思的：如果我们碰到了and， 那么我们需要解析n个case， 此时当我们解析了第一个case， 然后我们记录下第一个【1，2，3】 然后到第二个
    # 第二个的current是【2，3，4】，这样一来我们就可以根据第一个的记录（tmp_index变量来决定是取交集还是取补集）
    def __parse_conditions(self, **conditions):
        # 如果条件为空,数据索引为所有
        if 'conditions' in conditions:
            conditions = conditions['conditions']

        if not conditions:
            match_index = range(0, self.__rows)
        else:
            name_tmp = self.__get_name_tmp(**conditions)
            match_tmp = list()
            match_index = list()
            is_first = True
            for field_name in name_tmp:
                data = self.__get_field_data(field_name)
                data_type = self.__get_field_type(field_name)
                case = conditions[field_name]
                if not isinstance(case, BaseCase):
                    raise TypeError('Type Error, value must be "Case"')

                if is_first:
                    length = self.__get_field_length(field_name)
                    for index in range(0, length):
                        if case(data[index], data_type):
                            match_tmp.append(index)
                            match_index.append(index)
                    is_first = False
                    continue

                for index in match_tmp:
                    if not case(data[index], data_type):
                        match_index.remove(index)

                match_tmp = match_index
                print(match_index, "!")
        return match_index


    def delete(self, **conditions):
        # 解析条件 返回符合条件的数据索引
        match_index = self.__parse_conditions(**conditions)

        # 遍历所有Field对象
        for field_name in self.__field_names:
            count = 0
            match_index.sort()
            tmp_index = match_index[0]
            for index in match_index:
                if index > tmp_index:
                    # 因为内部删除api用的是pop 所我们需要从前往后删 然后每次删的时候因为有一个pop操作 所以需要往后加一个
                    index -= count

                self.__get_field(field_name).delete(index)
            count += 1
        self.__rows = self.__get_field_length(self.__field_names[0])


    def __get_field_length(self, field_name):
        field = self.__get_field(field_name)
        return field.length()


    def update(self, data, **conditions):
        match_index = self.__parse_conditions(**conditions)
        name_tmp = self.__get_name_tmp(**data)
        for field_name in name_tmp:
            for index in match_index:
                self.__get_field(field_name).modify(index, data[field_name])

    # 判断字段合理性
    def __get_name_tmp(self, **options):
        name_tmp = list()
        params = options
        for field_name in params.keys():
            if field_name not in self.__field_names:
                raise Exception("%s Field Not Exists" % field_name)
            name_tmp.append(field_name)
        return name_tmp

    def insert(self, **data):
        # 解析参数
        if 'data' in data:
            data = data['data']

        name_tmp = self.__get_name_tmp(**data)
        for field_name in self.__field_names:
            value = None
            # 如果存在该字段 赋值给value
            if field_name in name_tmp:
                value = data[field_name]
            # 如果不存在,则添加一个空值保持该字段长度与其他字段长度相等
            try:
                self.__get_field(field_name).add(value)
            except Exception as e:
                raise Exception(field_name, e)

            # 数据长度加1

        self.__rows += 1

    # 序列化与反序列化
    def serialized(self):
        data = {}
        for field_name in self.__field_names:
            data[field_name] = self.__field_objs[field_name].serialized()

        return SerializedInterface.json.dumps(data)

    @staticmethod
    def deserialized(data):
        json_data = SerializedInterface.json.loads(data)
        table_obj = Table()
        field_names = [field_name for field_name in json_data.keys()]
        for field_name in field_names:
            field_obj = Field.deserialized(json_data[field_name])
            table_obj.add_field(field_name, field_obj)
        return table_obj



