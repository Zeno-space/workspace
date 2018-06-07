import os
import json

"""实现了使用json文件为数据库的，增删改查功能，find、add、del、update

1、系统关键字：find、add、del、update、from staff_table、set、where暂时仅支持小写字母；
2、数据内容区分大小写；
3、单文件、无异常，后续扩展空间比较大。特别在分词这块。

函数：
    数据库函数：
        save_db(file_path=db_file)
        load_db(file_path=db_file)
        init_db()
    索引控制函数：
        id_increase()
        push_message(count, message)
        pull_message()
    数据库操作函数（增、删、改、查）：
        staff_add(info)
        staff_del(id_set)
        staff_update(id_set, info_dict)
        staff_find(id_set, cols)
    命令行分词函数：
        where(condition_dict, compare_list, operator_list = [])
        split_cmd
"""
#保存了一份初始员工信息文件，用于实验数据错乱后恢复。
db_file = r'staff_table.json'
db_file_init = r'staff_table_init.json'

#员工信息表，在运行过程全程保存在内存中（staff_table全局变量）
#维护两个索引（ID，phone）,以及一个消息队列
staff_table = {}
columns = ['id', 'name', 'age', 'phone', 'dept', 'enroll_date']
id_index = []
phone_index = []

message_tmp = {'count': 0, 'message': []}


def save_db(file_path=db_file):
    """把员工信息保存为'staff_table.json'文件
    """
    global staff_table

    with open(file_path, 'w', encoding='UTF-8') as staff_table_f:
        json.dump(staff_table, staff_table_f, ensure_ascii=False, indent=4)


def load_db(file_path=db_file):
    """读取用户信息（id,name,age,phone,dept,enroll_date）
    """
    global staff_table, id_index, phone_index

    with open(file_path, 'r', encoding='UTF-8') as staff_table_f:
        staff_table = json.load(staff_table_f)
        if staff_table:
            staff_table = {int(key): staff_table[key]
                           for key in staff_table
                           }  #json只能存储str格式的key，加载时转换回int

            phone_index = [staff_table[key]['phone'] for key in staff_table]
            id_index = list(staff_table.keys())
        else:
            push_message(0, '员工信息表为空，请输入“init”初始化或使用“add”命令添加数据')


def init_db():
    """通过'staff_table_init.json'文件初始化还原'staff_table.json'文件数据库
    """
    load_db(db_file_init)
    save_db()

    push_message(len(staff_table), '从init文件中还原实验数据成功')


def id_increase():
    """
    提供最新id
    """
    new_id = max(id_index) + 1
    id_index.append(new_id)
    return new_id


def push_message(count, message):
    """把消息推送到消息队列，count是影响到的记录数，message是具体消息。
    """
    message_tmp['count'] += count
    message_tmp['message'].append(message)


def pull_message():
    global message_tmp

    count = message_tmp['count']
    message = message_tmp['message']

    message_tmp = {'count': 0, 'message': []}

    return count, message


def staff_add(info):
    """添加新员工信息

    1、检测新员工手机号是否重复，唯一则允许添加；
    2、新员工id自增+1,并添加传入的新员工信息列表（不包含id），并返回成功信息；
    3、并保存到文件中。

    参数：
        info：新员工信息列表
    
    返回：
        new_id，添加成功返回新员工id号，失败False
    """
    if len(info) == 5:
        if info[2] not in phone_index:
            new_id = id_increase()  #新员工id自增

            employee = {}
            for i, c in enumerate(columns[1:]):
                employee[c] = info[i]
            staff_table[new_id] = employee
            
            phone_index.append(info[2])

            push_message(1, '%s号新员工信息添加成功'% new_id)
            save_db()
            return new_id
        else:
            push_message(0, '手机号已存在')
            return False
    else:
        push_message(0, '新员工信息列数不匹配')


def staff_del(id_set):
    """删除对应id的员工信息，并保存到文件
    """
    for id in id_set:
        del staff_table[id]

        id_str_list = [str(id) for id in id_set]
        if id_str_list:
            push_message(len(id_set), ','.join(id_str_list) + ' 号员工信息删除成功')
        else:
            push_message(0, '无删除条目')
    
    save_db()


def staff_update(id_set, info_dict):
    """
    """
    if info_dict.get('phone') and info_dict['phone'] in phone_index:
        push_message(0, '手机号已存在')
        return False
    elif not set(info_dict.keys()).issubset(set(columns)):
        push_message(0, '提交的修改项中含有未知列')
    else:
        for id in id_set:
            for key in info_dict:
                staff_table[int(id)][key] = info_dict[key]

        id_str_list = [str(id) for id in id_set]
        if id_str_list:
            push_message(len(id_set), ','.join(id_str_list) + ' 号员工信息已修改')
        else:
            push_message(0, '修改结果空')
        save_db()
        return True


def staff_find(id_set, cols):
    """
    """
    if cols[0] == '*':
        cols = columns

    result = []
    for row, id in enumerate(id_set):
        result.append([])
        for c in cols:
            if c == 'id':
                result[row].append(id)
            else:
                result[row].append(staff_table[id][c])
        push_message(1, result[row])

    id_str_list = [str(id) for id in id_set]
    if id_str_list:
        push_message(0, '查询结果为ID: ' + ','.join(id_str_list) + ' 号员工信息')
    else:
        push_message(0, '查询结果空')


def where(condition_dict, compare_list, operator_list = []):
    """将condition字典内的值与staff_table内的相应值做compare（逻辑运算，like）返回符合条件的id。

    可以处理复杂的多重逻辑与集合运算，例 where dept like IT and age = 22;
    
    参数：
        condition_dict = {column:value, ...}   键值对数目与compare_list相等。
            例中应当传入 {'dept': 'IT', 'age': 22}
        
        compare_list = [compare_operator, ...]  列表元素数量与condition_dict键值对相等。
            例中应当传入 {'like', '='}

        operate_list = [logical_operate, ...]  列表元素数量比condition_dict键值对少1个。
            例中应当传入 {'and'}
    """
    from functools import reduce

    def compare(value_s, value_t, op):
        """比较传入参数value_s，与staff_table内的value_t，是否符合op关系（大小，等于，like）。
        """
        if op in ['=', '>', '<', '>=', '<=']:
            op = '==' if op == '=' else op
            if isinstance(value_t, str) and isinstance(value_s, str):
                eval_str = '\'%s\''% value_s + op + '\'%s\''% value_t
            else:
                eval_str = str(value_s) + op + str(value_t)
            return True if eval(eval_str) else False
        elif op == 'like':
            return True if value_s in value_t else False

    def __get_operate(operator_list=operator_list):
        """依次取出operate_list内的逻辑操作符，供logical_op函数调用用于集合运算。
        """
        operator = operator_list[0]
        operator_list = operator_list[1:]
        return operator

    def logical_op(x_set, y_set):
        """根据__get_operate函数提供的逻辑操作字符，转化为相应的逻辑操作。
        
        参数：
            x_set,y_set: 是根据每次遍历condition_dict与compare_list运算获得的集合。
            例中的结果是 x_set = {1, 3, 5, 9}，y_set = {8, 1},本函数仅使用"and"操作符
            运算结果为 {1}
        """
        operate = __get_operate()

        if operate == 'and':
            return x_set & y_set
        elif operate == 'or':
            return x_set & y_set
        else:
            return x_set

    #分别计算condition_dict中的每一个条件与staff_table内的值进行比较运算的结果集
    #存入id_set_list
    if condition_dict:
        id_set_list = []
        for key, cmp in zip(condition_dict, compare_list):
            id_set_inner = set()
            id_set_list.append(id_set_inner)
            for id in staff_table:
                source = condition_dict[key]
                targe = staff_table[id][key] if key != 'id' else id
                if compare(source, targe, cmp):
                    id_set_inner.add(id)

        id_set = reduce(logical_op, id_set_list)  #集合运算
    else:
        id_set = set(id_index)     #没有条件，则返回全部ID

    return id_set  #返回符合条件的ID集合


def split_cmd(cmd):
    cmd = cmd.strip(' \n').split(' ', 1)
    cmd_head, cmd_body = cmd if len(cmd) > 1 else [cmd[0],[]]
    cmd_head = cmd_head.lower()

    def split_where(where_str):
        condition_dict = {}
        operator_list = []

        cmp_str = where_str.strip()    #仅一组逻辑运算，需补充
        key, value, operator = split_cmp(cmp_str)

        condition_dict[key] = value
        operator_list.append(operator)

        id_set = where(condition_dict, operator_list)
        return id_set

    def split_cmp(cmp_str):
        operator = ['=', '>', '<', '>=', '<=', 'like']
        for op in operator:
            if op in cmp_str:
                key, value = cmp_str.split(op)
                return key.strip(' \'\"'), value.strip(' \'\"') , op

    def split_cols(cols_str):
        cols = cols_str.strip().split(',')
        return cols

    if cmd_head in ['q', '退出']:
        exit()
    elif cmd_head == 'init':
        init_db()

    elif cmd_head == 'find':
        cols_str, where_str = cmd_body.split('from staff_table where')
        cols = split_cols(cols_str)
        id_set = split_where(where_str)
        staff_find(id_set, cols)

    elif cmd_head == 'add':
        cols_str = cmd_body.split('staff_table')[1]
        info = split_cols(cols_str)
        staff_add(info)

    elif cmd_head == 'del':
        where_str = cmd_body.split('from staff where')[1]
        id_set = split_where(where_str)
        staff_del(id_set)

    elif cmd_head == 'update':
        info_dict = {}
        cmp_str, where_str = cmd_body.split('set')[1].split('where')
        id_set = split_where(where_str)
        key, value, cmp = split_cmp(cmp_str)
        info_dict[key] = value
        staff_update(id_set, info_dict)
    else:
        push_message(0, '该命令还未设置，请查看命令输入是否出错')


if __name__ == '__main__':
    load_db()
    print('\n'.join(pull_message()[1]))
    while True:
        print(
            "1、find：例 find * from staff_table where age > 22",
            "2、add: 例 add staff_table Alex Li,25,134435344,IT,2015‐10‐29",
            "3、del: 例 del from staff where id=3",
            "4、update: 例 update staff_table set dept='Market' where dept = 'IT'",
            "5、init：还原所有实验数据", "6、q：退出程序",sep='\n')
        cmd = input('\n>>>')
        if not cmd:
            continue
        split_cmd(cmd)
        count, message = pull_message()
        for m in message:
            print(m)
        print('共影响条目%s条\n' % count)
