# -*- coding:utf-8 -*-
# import os
# def get_all_friends_img(picDir='friends'):
#     if not os.path.isdir(picDir):
#         print 0
#     else:
#         print 1
#     # os.makedirs(picDir)
# get_all_friends_img()
import urllib2
from bs4 import BeautifulSoup
import re
import json

def getArticleOrComment(Url,flag=True):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    request = urllib2.Request(url=Url, headers=headers)
    try:
        response = urllib2.urlopen(request)
        if flag:
            content = response.read().decode('utf8')
        else:
            content = response.read()
        
    except Exception, e:
        content = None
    return content

articlePage = getArticleOrComment('http://huaban.com/boards/17375733/?md=newbn&beauty')
# soupArticle = BeautifulSoup(articlePage, 'html.parser')
# print articlePage
appPins = re.findall(r'"pins":.*',articlePage)

result = json.loads(appPins[0][7:-2])
print len(result)
for i in result:
    url_pin = 'http://huaban.com/pins/%s/'%str(i['pin_id'])
    print url_pin
    # inPage = getArticleOrComment(url_pin)
    # keys = re.findall(r'"key":"(\w+-\w+)",',articlePage)
    url_pin2 = 'http://img.hb.aicdn.com/%s_fw658'%i["file"]["key"]
    f = open(str(i['pin_id'])+'.'+i["file"]["type"][6:],'wb')
    f.write(getArticleOrComment(url_pin2,False))
    f.close()

