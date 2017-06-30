from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator



d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'constitution2.txt'), encoding='utf-8').read()

# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = np.array(Image.open(path.join(d, "heart-mask.jpg")))


# wc = WordCloud(background_color="white", mask=alice_coloring, font_path=path.join(d, 'STXINGKA.TTF'),
#                max_font_size=60, width=1200, height=1000)
# # generate word cloud
# wc.generate(text)

# # create coloring from image
# image_colors = ImageColorGenerator(alice_coloring)

wordcloud = WordCloud(font_path=path.join(d, 'STXINGKA.TTF'),random_state=100,mask=alice_coloring, min_font_size=8,max_font_size=100, width=900, height=900, background_color=(255, 255, 255)).generate(text)
image = wordcloud.to_image()
image.show()
