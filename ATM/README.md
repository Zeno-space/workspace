
1、db和log，存放具体的数据库文件和日志文件；
    1、bank_db.json 为银行数据库
    2、sm_db.json 为购物商场数据库
    3、debug.log 为内部debug使用日志
    4、operation.log 为系统操作日志
    5、consumption.log 为消费日志,使用TimeRotatingFileHandler，30日时间回滚。

2、每个应用中，如bank、shopping_mall文件夹中实现接口封装；
    1、bank实现接口：
        1、show_account() 查看当前登录账户；
        2、consume(goods, price, number) 使用该接口进行消费
        3、withdraw(amount) 信用卡提现
        4、repay(amount) 信用卡还款
        5、deposit(amount) 储蓄卡存款
        6、transfer(amount, username) 储蓄卡用户名之间转账
3、core中实现共用的代码，如日志，数据库的代码接口；

4、manage.py实现的是菜单列表与应用接口返回内容的的展示；
    1、具体的递归菜单在menu变量中；
    2、如果菜单中的key在mapping中找到对应的函数，则调用该函数，并判断函数的返回值，
    3、返回值为真，继续停留在当前目录，否则进入下个目录。

5、到项目目录下运行python manage.py开始程序。
