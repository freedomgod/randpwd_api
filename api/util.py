import random
import string
import pyperclip


def rand_pin(para: dict) -> list:
    """
    依据参数生成随机字符串
    param length: 字符串长度
    param special: 是否包含特殊的字符串，可选值有0, 1, 2, 3，分别表示不包含、包含特殊字符、包含标点、包含特殊字符和标点，默认为0
    param capt: 字母大写的个数
    param key: 包含关键字
    param number: 生成密码的个数
    :return: 字符串列表
    """
    digits = list('0123456789')  # 数字
    alph = list('abcdefghijklmnopqrstuvwxyz')  # 字母
    dots = list(',./?;:\'"[]{}\\|')  # 标点
    op = list('!@#$%^&*()_+=-~`')  # 特殊符号
    st_pool = digits + alph  # 基础字符池

    special = para.get('s')
    length = para.get('l')
    capt = para.get('c')
    key = para.get('k')
    n = para.get('n')

    if special == 0:  # 添加额外的字符
        pass
    elif special == 1:
        st_pool += op
    elif special == 2:
        st_pool += dots
    else:
        st_pool += dots + op

    pin = []
    for i in range(n):
        pin_lis = []
        if key is None:
            if capt >= length:
                pin_lis += [random.choice(st_pool).upper() for _ in range(length)]
            else:
                capt_st = [random.choice(string.ascii_uppercase) for _ in range(capt)]
                pin_lis += [random.choice(st_pool) for _ in range(length - capt)]
                pin_lis += capt_st
        else:
            if (len(''.join(list(key))) + capt) >= length:
                pin_lis += list(key)
            else:
                capt_st = [random.choice(string.ascii_uppercase) for _ in range(capt)]
                pin_lis += [random.choice(st_pool) for _ in range(length - len(''.join(key)) - capt)] + capt_st + key
        random.shuffle(pin_lis)
        tmp = ''.join(pin_lis)
        pin.append(tmp)
    pyperclip.copy(pin[0])  # 自动复制生成的第一条密码
    return pin
