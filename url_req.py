# -*- coding=utf-8 -*-
import json
import os
import os.path
import re
from urllib import parse, request
for i in range(22,40):
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=529833412390&spuId=529766240&sellerId=2261134338&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=1&ua=007UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FS3RLf0V5RXpAfCo%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhcY1xoUm5SbVdrXGFDeER7RXpDf0J5RHpAfkd%2FUQc%3D%7CVWldfS0TMww3AyMfJwcpVTgOeht1UW5IMlgxTHxMYjRi%7CVmhIGCUFOBgkGyMWNgo2DjQLKxcjHCEBPQA1CCgUIB8iAj4DOgdRBw%3D%3D%7CV25OHjAePgoxCSkVKxEvDzMLNgo2YDY%3D%7CWGFBET8RMQU8AiIbIxwmBjkEOQM3YTc%3D%7CWWBAED4QMAUwDCwVKRMuDjEOMAwxZzE%3D%7CWmJCEjwSMmJWaFR0TXFOdlZiX2FBeUB7WWVQalJyRnpaZFAGJhs7FTsbJBolHyRyJA%3D%3D%7CW2JfYkJ%2FX2BAfEV5WWdfZUV8XGBdfUlpXHxAey0%3D&isg=AsDAvwStjd-bLnHXbaBDRxIKkU5S4aXn0l1NFzpQNFtytWXf41jVo0bHuyqP&itemPropertyId=&itemPropertyIndex=&userPropertyId=&userPropertyIndex=&rateQuery=&location=&needFold=0&_ksTS=1499229734694_3873&callback=jsonp3874'
    url = url.format(i)
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    with request.urlopen(req) as f:
        res_str = f.read().strip().decode('GBK')
        json_str = res_str[10:-1]
        # print(json_str)
        mh = re.findall(r'(//img.alicdn.com.*?\.jpg)',json_str)
        n = 1
        for imgUrl in mh:
            req = request.Request('https:'+imgUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
            with request.urlopen(req) as f:
                content = f.read()
                imageName = os.path.join("G:/images", "{}_{}.jpg".format(i,n) )
                with open(imageName, 'wb') as fp:
                    fp.write(content)
                n+=1
