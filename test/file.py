# -*- coding:utf-8 -*-
import os
def get_all_friends_img(picDir='friends'):
    if not os.path.isdir(picDir):
        print 0
    else:
        print 1
    # os.makedirs(picDir)
get_all_friends_img()
