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
    result = {}
    for id in id_set:
        for c in col:
            result[id] = {}
            result[id][c] = staff_table[id][c]

def where(condition):
    id_set = ()
    return id_set

def split_word(cmd):
    pass


if __name__ == '__main__':
    load_db()
    staff_add('a')
