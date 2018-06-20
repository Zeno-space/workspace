from core.json_db import JsonDb
from conf.setting import BANK_DB_PATH
from core.logger import debug_log

#0:'用户名不存在',1：'密码错误'
AUTH_ERROR = {
    0:'用户名不存在',
    1:'密码错误'
}
bank_db = JsonDb(BANK_DB_PATH,'username')

user_data = {}
"""
'username': None,
'password':None,
'status':False,
'balance':0,
'credit limit':0
"""

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
        while user_data:
            result = authenticate()
            debug_log.error(AUTH_ERROR[result])
        else:
            user_data = result
        return func(*args, **kwargs)
    return inner

def registe(username, password, balance):
    # username = input('用户名：')
    # password = input('密码：')
    # balance = int(input('请输入您的预存金额：'))

    user_data = {}
    user_data['username'] = username
    user_data['password'] = password
    user_data['status'] = 1
    user_data['balance'] = balance
    user_data['credit limit'] = 15000
    bank_db.add(user_data)

    return True

@login
def show_account():
    pass

def consume(goods, price, number):
    pass

def withdraw(amount):
    pass

def repay(amount):
    pass

def deposit(amount):
    pass

def transfer(amount, user):
    pass

