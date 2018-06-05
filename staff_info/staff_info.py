import os
import json

db_file = r'staff_table.json'
db_file_init = r'staff_table_init.json'


def save_db(table, file_path=db_file):
    """把员工信息保存为'staff_table.json'文件
    """
    with open(file_path, 'w', encoding='UTF-8') as staff_table_f:
        json.dump(table, staff_table_f, ensure_ascii=False, indent=4)


def load_db(file_path=db_file):
    """读取用户信息（id,name,age,phone,dept,enroll_date）
    """
    if os.path.getsize(file_path):
        with open(file_path, 'r', encoding='UTF-8') as staff_table_f:
            staff_table = json.load(staff_table_f)
            staff_table = {int(key): staff_table[key] for key in staff_table}

            # 在staff_table中，key为0的value包含两个索引（id_index,phone_index）
            staff_table[0] = {}
            id_index = sorted(list(staff_table.keys()))
            staff_table[0]['id_index'] = id_index
            staff_table[0]['phone_index'] = [
                staff_table[key]['phone'] for key in id_index[1:]
            ]

    else:
        staff_table = {}
    return staff_table


def init_db():
    """通过'staff_table_init.json'文件初始化还原'staff_table.json'文件数据库
    """
    staff_table = load_db(db_file_init)
    save_db(staff_table, db_file)


def db_add(staff_table,info):
    pass

def db_del(staff_table,id):
    pass

def db_update(staff_table,id,info):
    pass

def split_word(cmd):
    pass

def find_info(staff_table,id,col = []):
    pass
    
def process_add():
    pass


def process_del():
    pass


if __name__ == '__main__':
    print(load_db())