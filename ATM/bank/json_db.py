import os, json


def load_db(DB_PATH):
    """加载json文件数据
    """
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='UTF-8') as db_file:
            data = json.load(db_file)

        return data
    else:
        save_db(None, DB_PATH)

        return None


def save_db(data, DB_PATH):
    """把员工信息保存为'staff_table.json'文件
    """
    with open(DB_PATH, 'w', encoding='UTF-8') as db_file:
        json.dump(data, db_file, ensure_ascii=False, indent=4)

    return True

def add(DB_PATH, records, increase=None):
    pass

def delete(DB_PATH,records_id):
    pass

def update(DB_PATH, records_id, record_sub):
    pass

def select(DB_PATH, records_id, colunms):
    pass


if __name__ == '__main__':
    from setting import BANK_DB_PATH
    print(load_db(BANK_DB_PATH))