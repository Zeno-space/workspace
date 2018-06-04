import os
import sys

if __name__ == '__main__':

    menu = {
        '北京': {
            '海淀': {
                '五道口': {
                    'soho': {},
                    '网易': {},
                    'google': {}
                },
                '中关村': {
                    '爱奇艺': {},
                    '汽车之家': {},
                    'youku': {},
                },
                '上地': {
                    '百度': {},
                },
            },
            '昌平': {
                '沙河': {
                    '老男孩': {},
                    '北航': {},
                },
                '天通苑': {},
                '回龙观': {},
            },
            '朝阳': {},
            '东城': {},
        },
        '上海': {
            '闵行': {
                "人民广场": {
                    '炸鸡店': {}
                }
            },
            '闸北': {
                '火车站': {
                    '携程': {}
                }
            },
            '浦东': {},
        },
        '山东': {},
    }

    exit_flag = True
    while exit_flag:
        print('-'.center(os.get_terminal_size().columns-2, '-'), '\n以下是第一级地区：\n')          #分隔符+level1提示
        for i_1, key_1 in enumerate(menu):
            print('%d、%s' % (i_1 + 1, key_1))
        province = input('\n请输入您想继续深入了解的地区中文名称，或输入”退出“、”返回上级“实现相应功能：\n>>>')
        if menu.get(province):
            print('以下是%s内的地区' % province)
            for i_2, key_2 in enumerate(menu[province]):
                print('%d、%s' % (i_2 + 1, key_2))
            break
        else:
            if province == '退出':
                exit
            else:
                print('请输入中文名称，例如：北京;如需退出请输入”退出“;返回上一级菜单，请输入”返回上一级“：\n>>>')

