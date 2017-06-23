# -*- coding:utf-8 -*-
import os
import Image
import math


# 拼接合成好友头像
def make_all_friends_img(image_list,width=120,height=120):
    images_count = len(image_list)
    n = int(math.ceil(pow(images_count, 0.5)))
    toImage = Image.new('RGBA', (width * n, height * n))
    for y in range(0,n):
        for x in range(0,n):
            print x*width,y*height
            fromImage = Image.open(image_list.pop())
            fromImage =fromImage.resize((width,height), Image.ANTIALIAS)
            toImage.paste(fromImage, (x*width, y*height))
            if len(image_list) == 0:
                toImage.save('all_friend.jpg')
                return 

dirf,f = os.path.split(os.path.abspath('.')) 
dirpath = os.path.join(dirf,'friends')
os.chdir(dirpath)
images = [x for x in os.listdir('.') if os.path.isfile(x)]

make_all_friends_img(images,width=100,height=100)
