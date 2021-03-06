
import os
from PIL import Image
import json
import urllib
import math

class image(object):
    def __init__(self, width=120, height=120):
        self.width = width
        self.height = height

    def get_image_list(self, path_str='G:/images'):
        os.chdir(path_str)
        images = [x for x in os.listdir(
            path_str) if os.path.isfile(os.path.join(path_str, x))]
        return images

    def getInfo(self,path_str):
        i = Image.open(path_str)
        return i 
        
    # 拼接合成好友头像
    def make_all_friends_img(self, image_list):
        if image_list is None:
            return
        images_count = len(image_list)
        n = int(math.ceil(pow(images_count, 0.5)))
        toImage = Image.new(
            'RGBA', (self.width * n, self.height * n), (255, 255, 255))
        for y in range(0, n):
            for x in range(0, n):
                print(x * self.width, y * self.height)
                try:
                    fromImage = Image.open(image_list.pop())
                    fromImage = fromImage.resize((self.width, self.height), Image.ANTIALIAS)
                    toImage.paste(fromImage, (x * self.width, y * self.height))
                except Exception as e:
                    pass
                if len(image_list) == 0:
                    toImage.save('all_friend.jpg')
                    return


if __name__ == '__main__':
    image = image()
    image.make_all_friends_img(image.get_image_list())