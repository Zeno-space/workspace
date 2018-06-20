from conf.setting import BANK_DB_PATH
from core.logger import debug_log
from core.json_db import JsonDb
from bank import bank
# from shopping_mall import shopping_mall


# db = JsonDb(BANK_DB_PATH, ['name'])
# db.add({'name':'zeno'})
# db.update('1', {'name':'zeno40'})
# print(db.select('1'))
mapping = {
    'registe':registe,
    'login':login,
    'account_info':show_account
}
menu_logged_in = {
    'bank': {
        'account_info':{},
        'withdraw':{},
        'repay':{},
        'deposit':{},
        'transfer':{},
    },
    'shopping_mall':{
        'goods':{
            'cart':{
                'pay':{}
            },
            'comsume_log':{}
        }
    }
}
menu_main = {
    'registe':menu_logged_in,
    'login':menu_logged_in
}

def registe():
    username = input('用户名：')
    password = input('密码：')
    balance = int(input('请输入您的预存金额：'))
    result = bank.registe(username, password, balance)
    if result:
        return menu_logged_in

def login():
    bank.login(bank.show_account)
    return menu_logged_in

def show_account():
    result = bank.show_account


def run(menu):
    while True:
        for i, key in enumerate(menu_main):
            print('%d、%s' % (i + 1, key))
        print('\n请输入指令前的代码，或输入“quit|退出”、“back|返回”实现相应功能：')
        cmd = input('>>>')




