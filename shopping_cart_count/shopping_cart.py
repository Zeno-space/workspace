import sys
import os
import json
import copy

#1、通过登录函数登录来加载用户资金与“历史购物车”，也可以通过输入未注册的账户，注册并初始化工资；
#2、打印商品列表后，可以通过代码来循环购买商品；
#3、选择商品后，会判断工资是否足够用于购买，足够则添加进“当前购物车”，不足弹出提示；
#4、可以输入“h”，来查看之前登录的所有购物情况（历史购物车）；
#5、也可以输入“q”退出程序，并打印“当前购物车”与账户工资余额，并高亮提示（仅支持Linux与部分IDE）；

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

json_file = 'users.json'

module_name = '购物车'
print(module_name.center(os.get_terminal_size().columns
     - len(module_name),'-'))  # 分隔线


def save_users(users):
    """把用户资料保存为json文件
    """
    with open(json_file, 'w', encoding='UTF-8') as f_users:
        json.dump(users, f_users, ensure_ascii=False, indent=4)


def load_users():
    """读取用户资料（用户名、密码、工资、历史购买记录）
    """
    if os.path.getsize(json_file):
        with open(json_file, 'r', encoding='UTF-8') as f_users:
            users = json.load(f_users)
    else:
        users = {}
    return users


def login():
    """通过该函数登陆，成功则返回：用户名、剩余工资、购物车

    使用json文件保存账户登陆信息与配置，数据结构为：
    {
        username: {
            "password": password,
            "salary": salary,
            "shopping_cart": {
                product_name: {
                    "price":price
                    "count":count
                }
            }
        }
    }
    登陆过程中，输入无效账户可以选择注册账户或者重新输入；
    """
    users = load_users()

    print("\n-------请根据相关提示输入信息登陆-------\n")

    while True:
        user = input('请输入用户名：')
        password = input('密码：')

        if users.get(user):
            correct_password = users[user]['password']
            if correct_password == password:
                salary = users[user]['salary']
                shopping_cart = users[user]['shopping_cart']
                print("\n-------登陆成功！欢迎回来%s-------\n" % user)
                return user, salary, shopping_cart
            else:
                print("\n%s密码错误，请重新输入\n" % user)
        else:
            # 陌生账号，提示是否注册。
            cmd = input('该账号未注册！是否注册该账户：%s\n' % user + '1、是\n' + '2、退出\n' +
                        '3、输入其他值重新登陆\n>>> ').strip()
            if cmd in ('1', '是', 'y', 'yes'):  # 注册新用户
                salary = int(input('请输入您的工资：'))
                users[user] = {}
                users[user]['password'] = password
                users[user]['salary'] = salary
                users[user]['shopping_cart'] = {}
                save_users(users)
                print("\n-------登陆成功！感谢你的支持，%s-------\n" % user)
                return user, salary, {}
            elif cmd in ('2', '退出', 'q'):  # 退出
                sys.exit(0)

            else:  # 重新输入
                continue


if __name__ == '__main__':
    user, salary, his_shopping_cart = login()  # 登陆
    shopping_cart = {}
    shopping_cart_all = copy.deepcopy(his_shopping_cart)

    print("\033[1;31;40m" + "  当前余额为:%s  " % salary +
          "\033[0m")  # "\n\033[1;31;40m" + str + "\033[0m"  linux下高亮，红色前景，黑色背景

    # 循环输出商品列表
    while True:
        s = '商品列表'
        print(s.center(os.get_terminal_size().columns - len(s), '*'))
        print(' ' * 3 + '品名' + ' ' * 8 + '价格\n')
        for i, product in enumerate(goods):
            print("%s、%-8s  %-5s" % (i + 1, product['name'], product['price']))

        # 根据代码购买商品
        choice = input("\n输入想买的商品编号;\n输入“h”或“历史记录”查看历史消费记录;" +
                       "\n输入“q”或“退出”退出完成结算,将显示您的当前购物车与余额:\n>>> ")
        if choice.isdigit():
            choice = int(choice) - 1
            if choice >= 0 and choice < len(goods):
                product = goods[choice]
                product_name = product['name']
                product_price = product['price']

                # 检测余额是否足够
                if product_price <= salary:

                    # 添加进当前购物车
                    if shopping_cart.get(product_name):  # 如果刚购买过了，只要计数+1
                        shopping_cart[product_name]['count'] += 1
                    else:
                        shopping_cart[product_name] = {}
                        shopping_cart[product_name]['price'] = product_price
                        shopping_cart[product_name]['count'] = 1
                    salary -= product_price
                    print("\n\033[1;31;40m  添加商品 “%s” 到购物车.  \033[0m" %
                          (product_name))

                    # 添加进总记录购物车
                    if shopping_cart_all.get(product_name):  # 如果历史购买过了，只要计数+1
                        shopping_cart_all[product_name]['count'] += 1
                    else:
                        shopping_cart_all[product_name] = {}
                        shopping_cart_all[product_name][
                            'price'] = product_price
                        shopping_cart_all[product_name]['count'] = 1

                else:
                    print("\n\033[1;31;40m  你的工资不够啦，买不起 %s！ \033[0m" %
                          product_name)  # 余额不足提醒
            else:
                print("商品不存在,请重新选择")

        elif choice in ('h', '历史记录'):  # 输入输入“h”或“历史记录”查看历史消费记录

            # 如果有历史购物记录就罗列出所有已购商品。
            if len(his_shopping_cart) > 0:

                # 历史记录
                s = '历史购买商品'
                print(s.center(os.get_terminal_size().columns - len(s), '*'))
                print("    品名      价格    数量\n")
                for index, product in enumerate(his_shopping_cart):
                    print("%-2s、%-6s  %-4s    %-4d" %
                          (index + 1, product,
                           his_shopping_cart[product]['price'],
                           his_shopping_cart[product]['count']))

        elif choice in ('q', '退出'):  # 输入"q"或"退出"结束购物

            # 如果有购买商品（包括历史购买）就罗列出所有已购商品与显示余额，并保存到json文件。
            if len(shopping_cart) > 0:

                # 保存
                users = load_users()
                users[user]['salary'] = salary
                users[user]['shopping_cart'] = shopping_cart_all
                save_users(users)

                # 购物记录
                print("-------你已购买以下商品-------\n")
                print("    品名      价格    数量\n")
                for index, product in enumerate(shopping_cart):
                    print("%-2s、%-6s  %-4s    %-4d" %
                          (index + 1, product, shopping_cart[product]['price'],
                           shopping_cart[product]['count']))
                print("\n\033[1;31;40m  当前余额为:%s  \033[0m" % salary)  # 余额
            break
