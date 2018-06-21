from core.json_db import JsonDb
from conf.setting import BANK_DB_PATH
from core.logger import debug_log

#0:'用户名不存在',1：'密码错误'

bank_db = JsonDb(BANK_DB_PATH, ['username'])

ERROR_CODE = {1: '账户已被冻结', 2: '用户名不存在', 3: '密码错误', 4: '信用卡额度不足'}

SERVICE_CHARGE = 0.05  # 手续费

id = ''
user_data = {}
"""
'username': None,
'password':None,
'status':0,
'balance':0,
'credit limit':0
"""


def authenticate():

    username = input('用户名：')
    password = input('密码：')
    id_set = bank_db.where(('username', username))
    if id_set:
        id = id_set.pop()
        user_data = bank_db.select(id)
        debug_log.debug("bank_db.select(id)'s result:%s" % user_data)
        count = user_data[id]['status']
        right_password = user_data[id]['password']
        if count > 0:
            if password == right_password:
                bank_db.update(id, {'status': 3})
                return 0, user_data[id]
            else:
                count -= 1
                bank_db.update(id, {'status': count})
                return 3, '%s %s,剩余次数%s' % (username, '密码错误', count)
        else:
            return 1, '%s %s' % (username, '账户已被冻结,登录其他账户或输入新用户名注册\n')
    else:
        cmd = input('用户名不存在,是否注册该账户\n' + '1、是\n' + '2、否\n' + '>>> ').strip()
        if cmd in ('1', '是', 'y', 'yes'):  # 注册新用户
            balance = int(input('请输入您的预存金额：'))
            registe(username, password, balance)

        return 2, ''


def login(func):
    def inner(*args, **kwargs):
        global user_data
        while not user_data:
            code, result = authenticate()
            if code in ERROR_CODE:
                debug_log.error(result)
            else:
                user_data = result
            debug_log.debug("authenticate()'s result:%s" % user_data)
        return func(*args, **kwargs)

    return inner


def registe(username, password, balance):
    # username = input('用户名：')
    # password = input('密码：')
    # balance = int(input('请输入您的预存金额：'))
    global user_data
    new_user_data = {}
    new_user_data['username'] = username
    new_user_data['password'] = password
    new_user_data['status'] = 3
    new_user_data['balance'] = balance
    new_user_data['credit limit'] = 15000

    id = bank_db.add(new_user_data)
    if id:
        new_user_data['id'] = id
        user_data = new_user_data
        return True
    else:
        False


@login
def show_account():
    """ 账户信息 """
    global user_data
    from copy import deepcopy
    result = deepcopy(user_data)
    debug_log.debug("show_account()'s result:%s" % result)
    del result['password']

    return result


@login
def consume(goods, price, number):
    """ 信用卡消费 """
    global user_data
    id = user_data['id']

    amount = price * number  # 计算需扣除的金额
    if amount <= user_data['credit limit']:
        user_data['credit limit'] -= amount

        # 保存变动
        bank_db.update(id, {'credit limit': user_data['credit limit']})
        return True
    else:
        return 4, "%s信用卡额度不足（剩%s，需%s），请先还款" % (
            user_data['username'], user_data['credit limit'], amount)


@login
def withdraw(amount):
    """ 信用卡提现 """
    global user_data
    id = user_data['id']

    amount = amount * (1 + SERVICE_CHARGE)  # 计算需扣除的金额
    if amount <= user_data['credit limit']:
        user_data['credit limit'] -= amount
        user_data['balance'] += amount  # 提现至储蓄卡余额

        # 保存变动
        bank_db.update(id, {'credit limit': user_data['credit limit']})
        bank_db.update(id, {'balance': user_data['balance']})
        return True
    else:
        return 4, "%s信用卡额度不足（剩%s，需%s），请先还款" % (
            user_data['username'], user_data['credit limit'], amount)


@login
def repay(amount):
    """ 信用卡还款 """
    global user_data
    id = user_data['id']

    balance = user_data['balance']
    if amount <= balance:
        if amount + balance < 15000:

            # 储蓄卡额度补充到信用卡额度中
            user_data['credit limit'] += amount
            user_data['balance'] -= amount

            # 保存变动
            bank_db.update(id, {'credit limit': user_data['credit limit']})
            bank_db.update(id, {'balance': user_data['balance']})
            return True
        else:
            return 5, "%s还款金额超过信用卡账单（还：%s，仅需：%s）" % (
                user_data['username'], amount,
                15000 - user_data['credit limit'])
    else:
        return 4, "%s储蓄卡额度不足（剩%s，需%s），请先存款" % (user_data['username'],
                                               user_data['balance'], amount)


@login
def deposit(amount):
    """ 储蓄卡存款 """
    global user_data
    id = user_data['id']

    user_data['balance'] += amount  # 存款至储蓄卡余额
    bank_db.update(id, {'balance': user_data['balance']})  # 保存变动


@login
def transfer(amount, username):
    """ 储蓄卡转账 """
    global user_data
    id = user_data['id']

    balance = user_data['balance']
    if amount <= balance:
        id_set = bank_db.where(('username', username))
        if id_set:
            peer_id = id_set.pop()
            user_data['balance'] -= amount  # 减少自己的储蓄卡余额

            peer_balance = bank_db.select(peer_id)['balance']

            # 保存变动
            bank_db.update(id, {'balance': user_data['balance']})
            bank_db.update(peer_id, {'balance': peer_balance + amount})
