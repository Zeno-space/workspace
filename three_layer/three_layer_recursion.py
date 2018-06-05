import os
import sys

#程序开始显示第一级列表，后续可以通过输入列表中展示的地名进入下一级；
#输入“退出”或“quit”将退出程序，“返回”或“back”将返回上一级；

#注意：如果输入地名后没有显示进一步详细列表，可以查看写menu结构，应该是到最后一层了，
#想控制主体代码在15行内，非需求就不做啦，不过为了显示直观加了点换行，还是超了。
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


def show_place_name(place_dict):
    while True:
        print()  #仅好看
        for i, key in enumerate(place_dict):
            print('%d、%s' % (i + 1, key))
        info = input('\n请输入您想继续深入了解的地区中文名称，或输入“退出”、“返回”实现相应功能：\n>>>')
        if place_dict.get(info):
            print('\n以下是%s内的地区:\n' % info)
            show_place_name(place_dict[info])
        elif info in ('退出', 'quit'):
            sys.exit(0)
        elif info in ('返回', 'back'):
            return
        else:
            print('\n提示：请输入中文名称，例如：北京；如需退出请输入“退出”;返回上一级菜单，请输入“返回”\n')
            continue


if __name__ == '__main__':
    print('-'.center(os.get_terminal_size().columns - 2, '-'))  #分隔线
    show_place_name(menu)
