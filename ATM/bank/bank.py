from core.json_db import JsonDb
from conf.setting import BANK_DB_PATH
from core.logger import debug_log

#0:'用户名不存在',1：'密码错误'
AUTH_ERROR = {
    0:'用户名不存在',
    1：'密码错误'
}
bank_db = JsonDb(BANK_DB_PATH,'username')

"""
'username': None,
'password':None,
'status':False,
'balance':0,
'credit limit':0
"""
user_data = {}

def authenticate():

    username = input('用户名：')
    password = input('密码：')
    id = bank_db.where('name',username)
    if id:
        user_data = bank_db.select(id)
        if user_data['password'] == password:
            return user_data
        else:
            return 1
    else:
        debug_log.error('%s用户名不存在'% username)
        return 0
    


def login(func):
    
    def inner(*args, **kwargs):
        global user_data
        if user_data:
            result = authenticate()
            if result in AUTH_ERROR.keys():


        return func(*args, **kwargs)
    return inner

def register(username, password):
    # 陌生账号，提示是否注册。
    # username = input('用户名：')
    # password = input('密码：')
    # balance = int(input('请输入您的预存金额：'))

    user_data = {}
    user_data['username'] = username
    user_data['password'] = password
    user_data['status'] = 1
    user_data['balance'] = balance
    user_data['credit limit'] = 15000
    bang_db.add(user)

    return True

