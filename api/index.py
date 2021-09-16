import flask
import json
import random
import string
from gevent import pywsgi
# from util import rand_pin

# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
app = flask.Flask(__name__)


def rand_pin(para: dict) -> list:
    """
    依据参数生成随机字符串
    param length: 字符串长度
    param special: 是否包含特殊的字符串，可选值有0, 1, 2, 3，分别表示不包含、包含特殊字符、包含标点、包含特殊字符和标点，默认为0
    param capt: 字母大写的个数
    param key: 包含关键字
    :return: 字符串
    """
    digits = list('0123456789')  # 数字
    alph = list('abcdefghijklmnopqrstuvwxyz')  # 字母
    dots = list(',./?;:\'"[]{}\\|')  # 标点
    op = list('!@#$%^&*()_+=-~`')  # 特殊符号
    st_pool = digits + alph  # 基础字符池

    special = para.get('special')
    length = para.get('length')
    capt = para.get('capital')
    key = para.get('key')
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
    return pin


# 'index'是接口路径，methods不写，默认get请求
# get方式访问
@app.route('/', methods=['get', 'post'])
def rand_pwd():
    # url参数格式：? l=20 & s=1 & c=1 & k=free
    # l 表示随机数的长度
    # s 表示是否包括标点符号等其他字符
    # c 表示字母是否有大写
    # k 表示是否包含关键字
    # n 表示生成的个数

    l = flask.request.args.get('l', 15)
    s = flask.request.args.get('s', 0)
    c = flask.request.args.get('c', 1)
    k = flask.request.args.getlist('k')
    n = flask.request.args.get('n', 1)
    para = {
        'length': int(l),
        'special': int(s),
        'capital': int(c),
        'key': k,
        'n': int(n)
    }
    res = {
        'pwd': rand_pin(para),
        'status': 200
    }
    return json.dumps(res, ensure_ascii=False)


server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
server.serve_forever()
app.run()
