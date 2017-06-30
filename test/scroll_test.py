# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time

browser1 = webdriver.Firefox()
str_url = ''
baseUrl = 'http://huaban.com/boards/19241298/'
browser1.get(baseUrl+str_url)
# browser1.execute_script("window.scrollBy(0,10000)")
for i in range(1,100):
    browser1.execute_script("window.scrollBy({},{})".format(0,(i)*500))
    time.sleep(1)
# browser1.close()
