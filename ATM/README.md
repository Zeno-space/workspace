银行，余额和信用卡额度
精度两位数，检测 
互转：还款，提现
登录：@login_bank
日志：@log_bank
错误代码：CODE
API

购物商城
消费，使用@login_bank

两套账户

tabulate

shopping_mall使用bank的login

购物完直接进入购物车
pay 并记录消费日志

1、db和log，存放具体的数据库文件和日志文件；
    1、bank_db.json 为银行数据库
    2、sm_db.json 为购物商场数据库
    3、debug.log 为内部debug使用日志
    4、operation.log 为系统操作日志
    5、consumption.log 为消费日志,使用TimeRotatingFileHandler，30日时间回滚。
2、每个应用中，如bank、shopping_mall文件夹中实现接口封装；
3、core中实现共用的代码，如日志，数据库的代码接口；
4、manage.py实现的是菜单列表与应用接口返回内容的的展示；
5、到项目目录下运行python manage.py开始程序。
