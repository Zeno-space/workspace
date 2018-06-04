import sys
import os
import json

#高亮、格式化对齐、历史查询、pep8

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
    "name": "化妆品",
    "price": 499
}]

json_file = 'users.json'

module_name = '购物车'
print(
    module_name.center(os.get_terminal_size().columns - len(module_name),
                       '-'))  #分隔线


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
    """通过该函数登陆，成功返回用户名与数据列

    使用json文件保存账户登陆信息与配置，数据结构为：
    {
        username: {
            "password": password,
            "salary": salary,
            "shopping_cart": [goods, price]
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
            cmd = input('该账号未注册！是否注册该账户：%s\n' % user + '1、是\n' + '2、退出\n' +
                        '3、输入其他值重新登陆\n>>> ').strip()
            if cmd in ('1', '是', 'y', 'yes'):  #注册新用户
                salary = int(input('请输入您的工资：'))
                users[user] = {}
                users[user]['password'] = password
                users[user]['salary'] = salary
                users[user]['shopping_cart'] = []
                save_users(users)
                print("\n-------登陆成功！感谢你的支持，%s-------\n" % user)
                return user, salary, []

            elif cmd in ('2', '退出', 'q'):  #退出
                sys.exit(0)

            else:  #重新输入
                continue


if __name__ == '__main__':
    user, salary, shopping_cart = login()  #登录

    print("\n\033[1;31;40m 当前余额为:%s \033[0m" % salary)

    #循环输出商品列表
    while True:
        s = '商品列表'
        print(s.center(os.get_terminal_size().columns - len(s), '*'))
        print("   品名    价格\n")
        for i, product in enumerate(goods):
            print("%s、%s    %s" % (i + 1, product['name'], product['price']))

        #根据代码购买商品
        choice = input("\n输入想买的商品编号,输入“q”或“退出”退出购买:\n>>> ")
        if choice.isdigit():
            choice = int(choice) - 1
            if choice >= 0 and choice < len(goods):
                product = goods[choice]
                product_name = goods[choice]['name']
                product_price = goods[choice]['price']

                #检测余额是否足够,足够的话从工资中扣除，不够的话重新购买
                if product_price <= salary:
                    shopping_cart.append(product)
                    salary -= product_price
                    print("\n\033[1;31;40m 添加商品 %s 到购物车. \033[0m" %
                          (product_name))
                else:
                    print("\n\033[1;31;40m 你的工资不够买%s，换个商品！\033[0m" %
                          product_name)  #余额不足提醒
            else:
                print("商品不存在")

        elif choice in ('q', '退出'):  #输入"q"或"退出"结束购物

            #如果有购买商品（包括历史购买）就罗列出所有已购商品与显示余额，并保存到json文件。
            if len(shopping_cart) > 0:
                users = load_users()
                users[user]['salary'] = salary
                users[user]['shopping_cart'] = shopping_cart
                save_users(users)
                print("-------你已购买以下商品-------\n")
                print("   品名    价格\n")
                for index, product in enumerate(shopping_cart):
                    print("%s、%s    %s" % (index + 1, product['name'],
                                           product['price']))
                print("\n\033[1;31;40m当前余额为:%s\033[0m" % salary)
            break
