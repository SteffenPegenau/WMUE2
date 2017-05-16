#!/usr/bin/python
import os

import pickle
import csv
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud

'''
data = {}
try:
    pkl_file = open('hosts.pkl', 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
except Exception as e:
    print("No file found")

text = ""
for host,count in data.items():
    text += ("'" + host + "'\n") * int(count)
'''

reader = csv.reader(open('hosts.csv', 'r'), delimiter=';')
d = {}
for k,v in reader:
    if not k == "host":
        d[k] = int(v)

#max_words=1628,relative_scaling=1,
wordcloud = WordCloud(width=900,height=500,normalize_plurals=False).generate_from_frequencies(d)
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.show()

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

wordcloud.recolor(color_func=grey_color_func, random_state=3)

wordcloud.to_file("wordcloud.png")
'''
f = open("wordcloudtext.txt", "w")
f.write(text)
f.close()

os.system("wordcloud_cli.py --text wordcloudtext.txt --stopwords=cloud_stopwords.txt --imagefile wordcloud.png")
'''
