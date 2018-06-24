import os
from conf.setting import SM_DB_PATH
from core.logger import debug_log, consumption_log
from core.json_db import JsonDb

sm_db = JsonDb(SM_DB_PATH, ['username'])
shopping_cart = {}
total_value = 0

goods = [{
    "name": "电脑",
    "price": 1999
}, {
    "name": "鼠标",
    "price": 10
}, {
    "name": "游艇",
    "price": 20
}, {
    "name": "美女",
    "price": 998
}, {
    "name": "宝石",
    "price": 2000
}, {
    "name": "化妆品111",
    "price": 499
}]


def shopping(balance):
    global shopping_cart, total_value, goods

    # 循环输出商品列表
    while True:
        s = '商品列表'
        print(s.center((os.get_terminal_size().columns - len(s)) // 4, '*'))
        print(' ' * 3 + '品名' + ' ' * 8 + '价格\n')
        for i, product in enumerate(goods):
            print("%s、%-8s  %-5s" % (i + 1, product['name'], product['price']))

        # 根据代码购买商品
        choice = input("\n输入想买的商品编号;" +
                       "\n输入“q”或“退出”退出商品添加,进入购物车:\n>>> ")
        if choice.isdigit():
            choice = int(choice) - 1
            if choice >= 0 and choice < len(goods):
                product = goods[choice]
                product_name = product['name']
                product_price = product['price']

                # 检测余额是否足够
                if product_price > balance:
                    print("\n\033[1;31;40m  注意：当前购物车总价值已超过信用卡余额！ \033[0m"
                          )  # 余额不足提醒

                # 添加进当前购物车
                if shopping_cart.get(product_name):  # 如果刚购买过了，只要计数+1
                    shopping_cart[product_name]['count'] += 1
                else:
                    shopping_cart[product_name] = {}
                    shopping_cart[product_name]['price'] = product_price
                    shopping_cart[product_name]['count'] = 1

                balance -= product_price
                total_value += product_price

                print("  已添加商品 “%s” 到购物车.  " % (product_name))
            else:
                print("商品不存在,请重新选择")

        elif choice in ('q', '退出'):  # 输入"q"或"退出"结束购物
            break