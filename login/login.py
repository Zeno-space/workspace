import sys
import msvcrt
import json

#使用json文件保存账户登陆信息与配置；
#登陆过程中，输入无效账户错误三次机会将推出程序，但不影响重新启动程序后的使用；
#每个用户有三次登陆机会，锁死后需要json文件修改配置:count数值为小于3。{user:[password,count]}
#用户登录成功后清零count值。

#没有注册账户等功能，后续写ATM的时候再添加。

if __name__ == '__main__':
    
    with open('users.json', 'r', encoding='UTF-8') as f_users:
        users = json.load(f_users)  #内部拥有两个用户，zhang和wang

    print('\n-------请根据相关提示输入信息登陆-------\n')

    count = 0
    while True:
        user = input('请输入用户名：')
        password = input('密码：')

        if users.get(user):
            if users[user][1] < 3:
                if users[user][0] == password:
                    users[user][1] = 0
                    with open('users.json', 'w', encoding='UTF-8') as f_users:
                        json.dump(users, f_users, ensure_ascii=False)

                    print('\n-------登陆成功！欢迎回来%s-------\n' % user)
                    print('由于没什么功能，按任意键退出......')
                    msvcrt.getch()
                    sys.exit(0)
                    break
                else:
                    users[user][1] += 1
                    with open('users.json', 'w', encoding='UTF-8') as f_users:
                        json.dump(users, f_users, ensure_ascii=False)
                    if users[user][1] < 3:
                        print('%s密码错误，你还有%d次机会' % (user, 3 - users[user][1]))
                    else:
                        print('密码错误超过3次，该账户处于锁定状态，\n按任意键退出......')
                        msvcrt.getch()
                        sys.exit(0)
            else:
                print('该账户处于锁定状态')
        else:
            chance = 2 - count
            if chance > 0:
                print('账号错误！请核实你的用户名，你还有%d次机会\n' % chance)
            else:
                print('陌生人，由于3次输错账号，现程序处于锁定状态！可以通过重启程序继续尝试。\n按任意键退出......')
                msvcrt.getch()
                sys.exit(0)
            count += 1
