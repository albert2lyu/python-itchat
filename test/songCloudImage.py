'''
通过用户id 获取网易云音乐用户听歌历史 
歌曲云图
'''

import time
from os import path
from selenium import webdriver
from bs4 import BeautifulSoup
from wordcloud import WordCloud

class SongCloudImage(object):
    baseUrl = 'http://music.163.com/#/user/songs/rank?id={}' 
    def __init__(self, user_id):
        self.user_id = user_id
        self.__url = SongCloudImage.baseUrl.format(user_id)
    
  
    def show(self,show=True,save=False):

        driver = webdriver.PhantomJS()
        # 打开链接
        driver.get(self.__url)
        time.sleep(2)
        # 选择iframe
        driver.switch_to.frame("g_iframe")
        # 执行js切换用户所有历史听歌记录
        driver.execute_script("document.getElementById('songsall').click()")
        time.sleep(2)
        # 获取页面源码
        html = driver.page_source
        # 解析源码
        soup = BeautifulSoup(html, 'html.parser')
        songlists = []
        text = ''
        for li in soup.find_all('li'):
            song_info = li.find(name='span', attrs='txt')
            if song_info:
                song = {'name': song_info.find('b').get_text(), 'singer': song_info.find_all(attrs='s-fc8')[-1].get_text(), 'score': int(li.find(name='span', attrs='bg').get('style')[6:-2])}
                songlists.append((song.get('name') + ' ') * song.get('score'))
        d = path.dirname(__file__)
        text = ' '.join(songlists)
        # print(len(text))
        wordcloud = WordCloud(font_path=path.join(d, 'STXINGKA.TTF'), max_font_size=60, width=800, height=600, background_color=(255, 255, 255)).generate(text)
        image = wordcloud.to_image()
        if show:
            image.show()
        if save:
            image.save('{}.jpg'.format(self.user_id))

if __name__ == '__main__':
    songCloudImage =  SongCloudImage(474879522)
    songCloudImage.show()

    
            
            
        
