from core.pickle_db import PickleDb
from conf.setting import USER_DB_PATH
from core.logger import debug_log


class Auth:
    menu = {
        '注册': 'registe',
        '登录': 'login',
        '登出': 'logout',
    }

    def __init__(self):
        self.user_db = PickleDb(USER_DB_PATH, ['username'])
        self.user_data = {}
        """ 
        {
            'username': '',
            'password': '',
            'role': '',
            'status': 3
        }
        """

    def authenticate(self):
        user_db = self.user_db

        username = input('用户名：')
        password = input('密码：')
        id_set = user_db.where(('username', username))
        if id_set:
            id = id_set.pop()
            user_data = user_db.select(id)
            count = user_data[id]['status']
            right_password = user_data[id]['password']
            if count > 0:
                if password == right_password:
                    user_db.update(id, {'status': 3})
                    user_data[id]['id'] = id
                    return 0, user_data[id]
                else:
                    count -= 1
                    user_db.update(id, {'status': count})
                    return 3, '%s %s,剩余次数%s' % (username, '密码错误', count)
            else:
                return 1, '%s %s' % (username, '账户已被冻结,登录其他账户或输入新用户名注册\n')
        else:
            cmd = input('用户名不存在,是否注册该账户\n' + '1、是\n' + '2、否\n' +
                        '>>> ').strip()
            if cmd in ('1', '是', 'y', 'yes'):  # 注册新用户
                self.registe(username, password)

            return 2, ''

    def login(self):
        def outer(func):
            def inner(*args, **kwargs):
                user_data = self.user_data
                while not user_data:
                    code, result = self.authenticate()
                    if code:
                        debug_log.error(result)
                    else:
                        user_data = result
                        debug_log.info("%s登录成功！" % user_data['username'])
                return func(*args, **kwargs)

            return inner

        return outer

    def logout(self):
        user_data = self.user_data

        username = user_data['username']
        user_data = {}
        debug_log.info("%s已退出登录！" % username)

        return True

    def registe(self, username='', password=''):
        if not username:
            username = input('用户名：')
            password = input('密码：')

        user_db = self.user_db
        user_data = self.user_data
        new_user_data = {}
        new_user_data['username'] = username
        new_user_data['password'] = password
        new_user_data['status'] = 3
        new_user_data['role'] = 'student'

        id = user_db.add(new_user_data)
        if id:
            new_user_data['id'] = id
            user_data = new_user_data
            debug_log.info("%s注册成功！" % user_data['username'])
            return True
        else:
            False
