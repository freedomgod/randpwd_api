import flask
import json
from gevent import pywsgi
from util import rand_pin

# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
app = flask.Flask(__name__)


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


# api.run(port=5000, host='127.0.0.1')
server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
server.serve_forever()
app.run()
