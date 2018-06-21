from conf.setting import BANK_DB_PATH
from core.logger import debug_log
from core.json_db import JsonDb
from bank import bank

# from shopping_mall import shopping_mall

# db = JsonDb(BANK_DB_PATH, ['name'])
# db.add({'name':'zeno'})
# db.update('1', {'name':'zeno40'})
# print(db.select('1'))


def registe():
    username = input('用户名：')
    password = input('密码：')
    balance = int(input('请输入您的预存金额：'))
    code = bank.registe(username, password, balance)
    if code:
        return True
    else:
        return False


def login():
    func = bank.login(bank.show_account)
    if func:
        func()
        return True
    else:
        print(1)
        return False


def show_account():
    result = bank.show_account()
    print()
    for key in result:
        print('%s : %s' % (key, result[key]))
    return True


def withdraw():
    return True


def repay():
    return True


def deposit():
    return True


def transfer():
    return True


def goods():
    return True


def cart():
    return True


def pay():
    return True


def comsume_log():
    return True


mapping = {
    'registe': registe,
    'login': login,
    'account_info': show_account,
    'withdraw': withdraw,
    'repay': repay,
    'deposit': deposit,
    'transfer': transfer,
    'goods': goods,
    'cart': cart,
    'pay': pay,
    'comsume_log': comsume_log
}
menu_logged_in = {
    'bank': {
        'account_info': {},
        'withdraw': {},
        'repay': {},
        'deposit': {},
        'transfer': {},
    },
    'shopping_mall': {
        'goods': {
            'cart': {
                'pay': {}
            },
            'comsume_log': {}
        }
    }
}
menu_main = {'registe': menu_logged_in, 'login': menu_logged_in}


def run(menu):
    while True:
        print()
        debug_log.debug('------------------------------')
        num_mapping = {}
        for i, key in enumerate(menu):
            i += 1
            num_mapping[i] = key
            print('%d、%s' % (i, key))
        print('\n请输入指令前的代码，或输入“q|quit|退出”、“b|back|返回”实现相应功能：')
        cmd = input('>>> ')

        # 如果输入值为数字，并且在代码范围内，就通过num_mapping找到相应的字符串，
        # 再通过mapping找到字符串对应的函数；然后通过menu进入对应字符串的下一级。
        if cmd.isnumeric() and int(cmd) >= 1 and int(cmd) <= len(menu):
            func_str = num_mapping[int(cmd)]
            if not func_str in mapping or mapping[func_str]():
                run(menu[func_str])
            else:
                continue 
        elif cmd in ('退出', 'quit', 'q'):
            exit(0)
        elif cmd in ('返回', 'back', 'b'):
            return
        else:
            print('\n提示：请输入数字，例如：1；如需退出请输入“quit”;返回上一级菜单，请输入“back”')
            continue


if __name__ == '__main__':
    run(menu_main)
