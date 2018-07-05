from core.auth import Auth

def auth():
    auth_obj = Auth()
    menu = auth_obj.menu

def view():
    pass

def method():
    pass

mapping = {
    '认证':auth,
    '视图':view,
    '方法':method
}
menu = {
    '认证':{
        '视图':{
            '方法':{}
        }
    }
}

def run(obj, menu):
    while True:
        print()
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
            attr_str = num_mapping[int(cmd)]
            if hasattr(obj, attr_str) or getattr(obj, attr_str)():
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
    # print(courses_system.__dict__['__file__'])
    # print(courses_system.__dict__['ManagerView']().__dir__())
    # print(courses_system.StudentView().method)
    auth = Auth()
    menu = auth.menu
    run(obj, menu)
