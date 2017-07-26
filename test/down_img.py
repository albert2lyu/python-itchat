# encoding: utf-8

import requests
import re
import os
import os.path


class HuabanCrawler():

    def __init__(self):
        self.homeUrl = "http://huaban.com/boards/17375733/"
        self.images = []
        if not os.path.exists('G:/images'):
            os.mkdir('G:/images')

    def __load_homePage(self):
        return requests.get(url=self.homeUrl).content

    def __make_ajax_url(self, No):
        return self.homeUrl + "?j527r6n1&max=" + No + "&limit=20&wfl=1"

    def __load_more(self, maxNo):
        return requests.get(url=self.__make_ajax_url(maxNo)).content

    def __process_data(self, htmlPage):
        prog = re.compile(r'"pins":.*')
        appPins = prog.findall(htmlPage.decode('utf-8'))
        null = None
        true = True
        false = False
        if appPins == []:
            return None
        # print appPins
        result = eval(appPins[0][7:-2])
        # print result
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://hbimg.b0.upaiyun.com/" + \
                i["file"]["key"] + "_fw658"
            if 'image' == i["file"]["type"][:5]:
                info['type'] = i["file"]["type"][6:]
            else:
                info['type'] = 'NoName'
            self.images.append(info)

    def __save_image(self, imageName, content):
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def get_image_info(self, num=20):
        self.__process_data(self.__load_homePage())
        for i in range((num - 1) // 20):
            self.__process_data(self.__load_more(self.images[-1]['id']))
        return self.images

    def down_images(self):
        print("{} image will be download".format(len(self.images)))
        for key, image in enumerate(self.images):
            print('download {0} ...'.format(key))
            try:
                req = requests.get(image["url"])
            except:
                print('error')
            imageName = os.path.join(
                "G:/images", image["id"] + "." + image["type"])
            self.__save_image(imageName, req.content)


if __name__ == '__main__':
    hc = HuabanCrawler()
    hc.get_image_info(90)
    hc.down_images()

