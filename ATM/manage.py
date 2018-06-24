from conf.setting import BANK_DB_PATH
from core.logger import debug_log
from core.json_db import JsonDb
from bank import bank
from shopping_mall import shopping_mall

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
        return False


def logout():
    bank.logout()
    return False


def show_account():
    result = bank.show_account()
    print()
    for key in result:
        print('%s : %s' % (key, result[key]))
    return True


def withdraw():
    amount = input("请输入你需要提现的金额（5%手续费）:\n>>> ")
    if amount.isnumeric():
        bank.withdraw(int(amount))
    return False


def repay():
    amount = input("请输入你需要还款的金额:\n>>> ")
    if amount.isnumeric():
        bank.repay(int(amount))
    return False


def deposit():
    amount = input("请输入你需要存款的金额:\n>>> ")
    if amount.isnumeric():
        bank.deposit(int(amount))
    return False


def transfer():
    amount = input("请输入你需要转账的金额:\n>>> ")
    username = input("请输入你需要存入的账户:\n>>> ")
    if amount.isnumeric():
        bank.transfer(int(amount), username)
    return False


def shopping():
    shopping_mall.shopping(bank.user_data['credit limit'])
    cart()
    return True


def cart():
    shopping_cart = shopping_mall.shopping_cart
    # 购物记录
    print("-------你已购买以下商品-------\n")
    print("品名      价格    数量\n")
    for product in shopping_cart:
        print("%-6s  %-4s    %-4d" % (product, shopping_cart[product]['price'],
                                      shopping_cart[product]['count']))
    print("总价值为：%s" % shopping_mall.total_value)
    print("当前信用卡剩余额度为%s" % bank.user_data['credit limit'])

    return True


def pay():
    from copy import deepcopy
    _shopping_cart = deepcopy(shopping_mall.shopping_cart)
    for product in _shopping_cart:
        price = _shopping_cart[product]['price']
        number = _shopping_cart[product]['count']
        result = bank.consume(product, price, number)
        if result:
            del shopping_mall.shopping_cart[product]
        else:
            print("%s,数量：%s消费失败！\n" % (product, number))
    shopping_mall.total_value = 0
    print("当前信用卡剩余额度为%s" % bank.user_data['credit limit'])

    return True


mapping = {
    'registe': registe,
    'login': login,
    'logout': logout,
    'account_info': show_account,
    'withdraw': withdraw,
    'repay': repay,
    'deposit': deposit,
    'transfer': transfer,
    'shopping_mall': shopping,
    'cart': cart,
    'pay': pay,
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
        'pay': {},
    }
}
menu_main = {
    'registe': menu_logged_in,
    'login': menu_logged_in,
    'logout': menu_logged_in
}


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
