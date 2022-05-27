import re
from xenondb.case import *

class SQLParser:
    def __init__(self):
        self.__pattern_map = {
            'SELECT':
                r'(SELECT|select)(.*)(FROM|from)(.*)',
            'UPDATE':
                r'(UPDATE|update)(.*)(SET|set)(.*)',
            'INSERT':
                r'(INSERT|insert)(INTO|into)(.*)\((.*)\)(VALUES|values)\((.*)\)',
        }

        self.__action_map = {
            'SELECT':self.__select,
            'UPDATE':self.__update,
            'DELETE':self.__delete,
            'INSERT':self.__insert,
            'USE':self.__use,
            'EXIT':self.__exit,
            'QUIT':self.__exit,
            'SHOW':self.__show,
            'DROP':self.__drop
        }

        self.SYMBOL_MAP = {
            'IN': InCase,
            'NOT_IN': NotInCase,
            '>': GreaterCase,
            '<': LessCase,
            '=': IsCase,
            '!=': IsNotCase,
            '>=': GAECase,
            '<=': LAECase,
            'LIKE': LikeCase,
            'RANGE': RangeCase

        }

    def __get_comp(self, action):
        # 返回一个re对象
        return re.compile(self.__pattern_map[action])

    def __select(self, statement):
        comp = self.__get_comp('SELECT')
        ret = comp.findall("".join(statement))
        if ret and len(ret[0]) == 4:
            fields = ret[0][1]
            table = ret[0][3]
            if fields != "*":
                fields = [field.strip() for field in fields.split(",")]
            return {
                'type': 'search',
                'fields': fields,
                'table':table
            }

        return None

# update table set a = 1
    def __update(self, statement):
        statement = ' '.join(statement)
        comp = self.__get_comp('UPDATE')
        ret = comp.findall(statement)
        if ret and len(ret[0]) == 4:
            data = {
                'type': 'update',
                'table': ret[0][1],
                'data': {}
            }
            # 找到要修改
            set_statement = ret[0][3].split(",")
            # data记录了要被修改的数据
            for s in set_statement:
                s = s.split("=")
                field = s[0].strip()
                value = s[1].strip()
                if "'" in value or '"' in value:
                    value = value.replace('"', '').replace("'", '').strip()
                else:
                    try:
                        value = int(value.strip())
                    except:
                        return None
                data['data'][field] = value
            return data
        return None

    def __insert(self, statement):
        # statement是列表数据 INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
        # 正则查找 生成data
        # 跟上面一样遍历
        comp = self.__get_comp(statement.join("INSERT"))
        ret = comp.findall(statement)
        if ret and len(ret[0]) == 6:
            data = {
                'type':'insert',
                'table':ret[0][2],
                'data':{

                }
            }
            fields = ret[0][3].split(",")
            values = ret[0][5].split(",")
            for i in range(len(fields)):
                field = fields[i].strip()
                value = values[i].strip()
                # 分别处理int和str的情况
                if "'" in value or '"' in value:
                    value.replace("'", "").replace('"', "").strip()
                else:
                    try:
                        value = int(value)
                    except:
                        return None
                data['data'][fields] = values
            return data
        return None

    def __use(self, statement):
        return {
            'type': 'use',
            'database':statement[1]
        }

    def __exit(self, _):
        return{
            'type': 'exit'
        }

    def __show(self, statement):
        kind = statement[1]
        if kind.upper() == 'DATABASES':
            return {
                'type': 'show',
                'kind': 'databases'
            }
        elif kind.upper() == 'TABLES':
            return {
                'type': 'show',
                'kind': 'tables'
            }

    def __drop(self, statement):
        kind = statement[1]
        if kind.upper() == 'DATABASES':
            return {
                'type': 'show',
                'kind': 'databases',
                'name': statement[2]
            }
        elif kind.upper() == 'TABLES':
            return {
                'type': 'show',
                'kind': 'tables',
                'name': statement[2]
            }

    def __filter_space(self, obj):
        ret = []
        for x in obj:
            if x.strip() == '' or x.strip() == 'AND':
                continue
            ret.append(x)
        return ret

# SQLexample: select * from xxx where aa == bb
# or quit / exit

    def parse(self, statement):
        tmp_s = statement
        # 如果有where操作符，把它分开（注意大小写），给到statement
        if 'where' in statement:
            statement = statement.split('where')
        elif 'WHERE' in statement:
            statement = statement.split('WHERE')
        # 基础sql语句都是空格隔开关键字，此处用空格分隔sql语句
        base_statement = self.__filter_space(statement[0].split(" "))
        if len(base_statement) < 2:
            if not len(base_statement):
                raise Exception('Syntax Error')
            if base_statement[0] not in ['exit', 'quit']:
                raise Exception('Syntax Error for %s' % tmp_s)
        # 在定义字典__action_map时，字典的键是大写字符，此处转换为大写格式
        action_type = base_statement[0].upper()
        if action_type not in self.__action_map:
            raise Exception('Syntax Error for: %s' % tmp_s)
        action = self.__action_map[action_type](base_statement)
        if action is None or 'type' not in action:
            raise Exception('Syntax Error for:' % tmp_s)

        # 处理condition
        action['conditions'] = {}
        conditions = None
        if len(statement) == 2:
            conditions = self.__filter_space(statement[1].split(" "))

        # 我他妈是不是还得告诉用户range里面不能有空格？？？？
        if conditions:
            for index in range(0, len(conditions), 3):
                field = conditions[index]
                symbol = conditions[index + 1].upper()
                condition = conditions[index + 2]
                if symbol == "RANGE":
                    condition_tmp = condition.replace("(", "").replace(")", "").split(",")
                    start = condition_tmp[0]
                    end = condition_tmp[1]
                    case = self.SYMBOL_MAP[symbol](start, end)
                elif symbol == "IN" or symbol == "NOT_IN":
                    condition_tmp = condition.replace("(", "").replace(")", "").split(",")
                    condition = condition_tmp
                    case = self.SYMBOL_MAP[symbol](condition)
                else:
                    case = self.SYMBOL_MAP[symbol](condition)
                action['conditions'][field] = case
            return action