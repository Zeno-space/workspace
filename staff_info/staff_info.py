import os
import json

db_file = r'staff_table.json'
db_file_init = r'staff_table_init.json'

staff_table = {}
id_index = []
phone_index = []


def save_db(table, file_path=db_file):
    """把员工信息保存为'staff_table.json'文件
    """
    with open(file_path, 'w', encoding='UTF-8') as staff_table_f:
        json.dump(table, staff_table_f, ensure_ascii=False, indent=4)


def load_db(file_path=db_file):
    """读取用户信息（id,name,age,phone,dept,enroll_date）
    """
    global staff_table, id_index, phone_index

    if os.path.getsize(file_path):
        with open(file_path, 'r', encoding='UTF-8') as staff_table_f:
            staff_table = json.load(staff_table_f)
            staff_table = {int(key): staff_table[key] for key in staff_table}   #json只能存储str格式的key，加载时转换回int

            phone_index = [staff_table[key]['phone'] for key in staff_table]
            id_index = staff_table.keys()


def init_db():
    """通过'staff_table_init.json'文件初始化还原'staff_table.json'文件数据库
    """
    save_db(load_db(db_file_init))

def id_increase():
    """
    提供最新id
    """
    new_id = max(id_index) + 1
    id_index.append(new_id)
    return new_id

def staff_add(info):
    """
    1、
    2、新员工id自增+1,并添加传入的新员工信息列表（不包含id），并返回成功信息
    3、并保存到文件中

    参数：staff_table
    """
    col = ['name', 'age', 'phone', 'dept', 'enroll_date']

    
    if info[2] not in phone_index:
        new_id = id_increase()     #新员工id自增

        employee = {}
        for i,c in enumerate(col):
            employee[c] = info[i]
        staff_table[new_id] = employee
        
        save_db(staff_table)
        return True,'添加成功'
    else:
        return False,'手机号已存在'

def staff_del(id_set):
    """删除对应id的员工信息，并保存到文件
    """
    for id in id_set:
        del staff_table[id]

    save_db(staff_table)


def staff_update(id_set, info_dict):
    """
    """
    if info_dict.get('phone') and info_dict['phone'] in phone_index:
        return False,'手机号已存在'
    else:
        for id in id_set:
            for key in info_dict:
                staff_table[int(id)][key] = info_dict[key]

        save_db(staff_table)
        return True,'ID:%s 修改成功'% id
        


def staff_find(id_set, col=[]):
    """
    """
<<<<<<< Updated upstream
    result = {}
    for id in id_set:
        for c in col:
            result[id] = {}
            result[id][c] = staff_table[id][c]
=======
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
    push_message(0, '查询结果为ID: ' + ','.join(id_str_list) + ' 号员工信息')


def where(condition_dict, compare_list, operate_list = []):
    """将condition字典内的值与staff_table内的相应值做compare（逻辑运算，like）返回符合条件的id。

    可以处理复杂的多重逻辑与集合运算，例 where dept like IT and age = 22;
    
    参数：
        condition__dict = {column:value, ...}   键值对数目与compare_list相等。
            例中应当传入 {'dept': 'IT', 'age': 22}
        
        compare_list = [compare_operate, ...]  列表元素数量与condition_dict键值对相等。
            例中应当传入 {'like', '='}

        operate_list = [logical_operate, ...]  列表元素数量比condition_dict键值对少1个。
            例中应当传入 {'and'}
    """
    from functools import reduce

    def compare(value_s, value_t, op):
        """比较传入参数value_s，与staff_table内的value_t，是否符合op关系（大小，等于，like）。
        """
        op = '==' if op == '=' else op
        if op in ['==', '>', '<', '>=', '<=']:
            return True if eval(str(value_s) + op + str(value_t)) else False
        elif op == 'like':
            return True if value_s in value_t else False

    def __get_operate(operate_list=operate_list):
        """依次取出operate_list内的逻辑操作符，供logical_op函数调用用于集合运算。
        """
        operate = operate_list[0]
        operate_list = operate_list[1:]
        return operate

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
                if compare(condition_dict[key], staff_table[id][key], cmp):
                    id_set_inner.add(id)

        id_set = reduce(logical_op, id_set_list)  #集合运算
    else:
        id_set = set(id_index)     #没有条件，则返回全部ID

    return id_set  #返回符合条件的ID集合
>>>>>>> Stashed changes

def where(condition):
    id_set = ()
    return id_set

def split_word(cmd):
<<<<<<< Updated upstream
    pass
=======
    cmd = cmd.strip(' \n').split(' ', 1)
    cmd_head, cmd_body = cmd if len(cmd) > 1 else [cmd[0],[]]
    cmd_head = cmd_head.lower()
    if cmd_head in ['q', '退出']:
        exit()
    elif cmd_head == 'init':
        init_db()
    elif cmd_head == 'find':
        cols_str, cmp_str = cmd_body.split(' from staff_table where ')

        cols = cols_str.strip().split(',')
        condition_key, cmp ,condition_value = cmp_str.split(' ')
        condition_dict = {}
        condition_dict[condition_key] = condition_value
        id_set = where(condition_dict, [cmp])
        staff_find(id_set, cols)
    elif cmd_head == 'add':
        cmd_body = cmd_body[11:].strip()
        info = cmd_body.split(',')
        staff_add(info)
    elif cmd_head == 'del':
        tmp, cmp_str = cmd_body.split(' where ')
        condition_key, cmp ,condition_value = cmp_str.split(' ')
        condition_dict = {}
        condition_dict[condition_key] = condition_value
        id_set = where(condition_dict, [cmp])
        staff_del(id_set)
    elif cmd_head == 'update':
        tmp, cmp_str = cmd_body.split(' where ')

        #dept='IT' 分词，where,condition_key, cmp ,condition_value = cmp_str.split(' ')使用空格分词也不严谨

        condition_key, cmp ,condition_value = cmp_str.split(' ')
        condition_dict = {}
        condition_dict[condition_key] = condition_value
        id_set = where(condition_dict, [cmp])
        # where()
        # staff_update()
    else:
        push_message(0, '该命令还未设置，请查看命令输入是否出错')
>>>>>>> Stashed changes


if __name__ == '__main__':
    load_db()
<<<<<<< Updated upstream
    staff_add('a')
=======
    print('\n'.join(pull_message()[1]))
    while True:
        print(
            "1、find：例 find * from staff_table where age > 22",
            "2、add: 例 add staff_table Alex Li,25,134435344,IT,2015‐10‐29",
            "3、del: 例 del from staff where id=3",
            "4、update: 例 update staff_table SET dept='Market' WHERE dept = 'IT'",
            "5、init：还原所有实验数据", "6、q：退出程序",sep='\n')
        cmd = input('>>>')
        if not cmd:
            continue
        split_word(cmd)
        count, message = pull_message()
        for m in message:
            print(m)
        print('共影响条目%s条\n' % count)
>>>>>>> Stashed changes
