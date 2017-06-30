

# from urllib import request
# req = request.Request('http://music.163.com/#/user/songs/rank?id=125090772')
# req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
# with request.urlopen(req) as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data.decode('utf-8'))
from os import path
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from bs4 import BeautifulSoup
from wordcloud import WordCloud

driver = webdriver.Firefox()
baseUrl = 'http://music.163.com/#/user/songs/rank?id=474879522'
driver.get(baseUrl)
time.sleep(3)
driver.switch_to.frame("g_iframe")
driver.execute_script("document.getElementById('songsall').click()")
time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
songlists = []
for li in soup.find_all('li'):
    song_info = li.find(name='span',attrs='txt')
    if song_info:
        song = {'name':song_info.find('b').get_text(),'singer':song_info.find_all(attrs='s-fc8')[-1].get_text(),'score':int(li.find(name='span',attrs='bg').get('style')[6:-2])}
        songlists.append(song)

# driver.close()

d = path.dirname(__file__)

with open(path.join(d, 'constitution2.txt'),'a',encoding='utf-8') as f:
    for x in songlists:
        f.write((x.get('name')+' ')*x.get('score') +'\n')


text = open(path.join(d, 'constitution2.txt'), encoding='utf-8').read()


wordcloud = WordCloud(font_path=path.join(d, 'STXINGKA.TTF'),
                      max_font_size=60, width=800, height=600,background_color=(255,255,255)).generate(text)

image = wordcloud.to_image()
image.show()
# image.save(fp='a.png')

