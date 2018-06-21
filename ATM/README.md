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

1、db和log，存放具体的数据库文件和日志文件；
2、每个应用中，如bank、shopping_mall文件夹中实现接口封装；
3、core中实现共用的代码，如日志，数据库的代码接口；
4、manage.py实现的是菜单列表与应用接口返回内容的的展示。