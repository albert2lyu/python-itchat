# -*- coding:utf-8 -*-
# 100000 文本类
# 200000 链接类
# 302000 新闻类
# 308000 菜谱类
# 40001 参数 key 错误
# 40002 请求内容 info 为空
# 40004 当天请求次数已使用完
# 40007 数据格式异常
import requests
codes_map = {
    100000: True,  # '文本类'
    200000: True,  # '链接类'
    302000: True,  # '新闻类'
    308000: True,  # '菜谱类'
    40001: True,  # '参数 key 错误'
    40002: True,  # '请求内容 info 为空'
    40004: True,  # '当天请求次数已使用完'
    40007: True,  # '数据格式异常'
}


def request_robot(info='hello', userid='123456', url='http://www.tuling123.com/openapi/api', key=''):
    res = requests.post(url, json={'key': key, 'userid': userid, 'info': info})
    if res.status_code == 200:
        data = res.json()
        return response_handle(**data)
    else:
        return '抱歉,稍等。。。'


def response_handle(**kw):
    code = kw.get('code', 40004)
    res_str = ''
    if code == 100000 or code == 200000:
        res_str = kw.get('text', '') + kw.get('url', '')
    elif code == 302000:
        news = kw.get('list')
        if isinstance(news, Iterable):
            for nw in news:
                res_str += (nw.get('article', '') + '\n' +
                            nw.get('detailurl', '') + '\n')
    elif code == 308000:
        news = kw.get('list')
        if isinstance(news, Iterable):
            for nw in news:
                res_str += (nw.get('name', '') + '\n' +
                            nw.get('detailurl', '') + '\n')
    else:
        res_str = kw.get('text', '')

    return res_str


print request_robot(info='北京天气')
print request_robot(info='上海到郑州火车')
