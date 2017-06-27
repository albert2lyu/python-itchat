# -*- coding:utf-8 -*-
import os
import sys
import time
import requests
import logging
import itchat
from itchat.content import *

# PYQuanPin== 'zhangsongsong'

autoDict = {'zhangsongsong': True, 'Caroline': True, 'tiankongzhicheng': True}
autoUserNames = {}


# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

# 注册地图 名片 通知 分享信息 回复方法


@itchat.msg_register([MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # if msg['User']['NickName'] == 'Caroline':
    if autoUserNames.has_key(msg['FromUserName']):
        f = open('msg.js', 'a')
        info = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
            autoUserNames[msg['FromUserName']] + " : " + \
            str(msg['Text']) + msg.get('Url', '') + "\n"
        f.write(info)
        f.close()
        logging.info(info)
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

# 注册文本信息 回复方法


@itchat.msg_register(TEXT)
def text_reply(msg):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if autoUserNames.has_key(msg['FromUserName']):
        f = open('msg.info', 'a')
        info = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
            autoUserNames[msg['FromUserName']] + " : " + \
            str(msg['Text']) + msg.get('Url', '') + "\n"
        f.write(info)
        f.close()
        logging.info(info)
        text = request_robot(info=msg['Text'], userid=msg['FromUserName'])
        itchat.send(text, msg['FromUserName'])


# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(TEXT, isGroupChat=True)
def groupchat_reply(msg):
    if not msg['IsAt'] and msg['User']['NickName'] == 'hehe':
        # 请求图灵机器人 获取要回复的内容
        text = request_robot(info=msg['Text'], userid=msg['FromUserName'])
        # 发送到群里
        itchat.send(text, msg['FromUserName'])
        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


# 在注册 图片 附件 语音 视频 信息 下载方法
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    logging.info('图片视频信息--------------')
    logging.info(msg)
    # file = '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(
    #     msg['Type'], 'fil'), msg['FileName'])
    # itchat.send(file)


# 拼接合成好友头像
def make_all_friends_img(image_list, width=120, height=120, save_name='all_friend.jpg'):
    images_count = len(image_list)
    n = int(math.ceil(pow(images_count, 0.5)))
    toImage = Image.new('RGBA', (width * n, height * n))
    for y in range(0, n):
        for x in range(0, n):
            print x * width, y * height
            fromImage = Image.open(image_list.pop())
            fromImage = fromImage.resize((width, height), Image.ANTIALIAS)
            toImage.paste(fromImage, (x * width, y * height))
            if len(image_list) == 0:
                toImage.save(save_name)
                return


# 获取所以好友头像
def get_all_friends_img(picDir='friends'):
    if not os.path.isdir(picDir):
        os.makedirs(picDir)
    for i, friend in enumerate(itchat.get_friends()):
        itchat.get_head_img(
            userName=friend['UserName'], picDir='%s/%d.png' % (picDir, i))


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


# 向图灵机器人发送请求 获取结果
def request_robot(info='hello', userid='123456', url='http://www.tuling123.com/openapi/api', key='0ee53f65c46a4206'):
    res = requests.post(url, json={'key': key, 'userid': userid, 'info': info})
    if res.status_code == 200:
        data = res.json()
        return response_handle(**data)
    else:
        return '抱歉,稍等。。。'


# 处理机器人返回的数据
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


def get_rooms_info():
    for i, friend in enumerate(itchat.get_chatrooms()):
        logging.info(friend)
    

def get_auto_friends_username():
    for i, friend in enumerate(itchat.get_friends()):
        if autoDict.has_key(friend['PYQuanPin']):
            autoUserNames[friend['UserName']] = friend['NickName']
        else:
            logging.info(friend['NickName'] +
                         '__PYQuanPin:' + friend['PYQuanPin'])


itchat.auto_login(loginCallback=get_auto_friends_username)
itchat.run()
