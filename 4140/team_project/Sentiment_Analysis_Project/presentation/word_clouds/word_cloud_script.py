import pandas as pd
import math
import numpy as np
import random
from PIL import Image

pd.options.display.max_columns = None

#df = pd.read_csv('../results/2018_sentiments_benz.csv')
#new_df = df

df = pd.read_csv('../results/all_sentiment.csv')
new_df = df[df['Year']==2018]

splt = new_df['Verbatim'].dropna().str.split()

words = []
for sentence in splt:
    for j in range(len(sentence)):
        words.append(sentence[j])

rel_words = []
for word in words:
    word = word.lower()
    if len(word) > 3 and any(char.isdigit() for char in word)==False and word!='have' and word!='been' and 'metallic' not in word and 'does' not in word and word!='don\'t' \
                     and word!='they' and word!='then' and word!='than'  and word!='this' and word!='that' and '.' not in word and ',' not in word and '!' not in word and '?' not in word:
        rel_words.append(word.lower())


import wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.corpus import stopwords
from operator import itemgetter

#nltk.download('punkt')

#mask = np.array(Image.open('./glc_profile.jpeg'))
#mask = np.array(Image.open('./x3_profile.jpg'))

finder = BigramCollocationFinder.from_words(rel_words)
bigram_measures = BigramAssocMeasures()
scored = finder.score_ngrams(bigram_measures.raw_freq)

scoredList = sorted(scored, key=itemgetter(1), reverse=True)

word_dict = {}
listLen = len(scoredList)

for i in range(listLen):
    word_dict[' '.join(scoredList[i][0])] = scoredList[i][1]

WC_height = 1000
WC_width = 1500
WC_max_words = 50

#wordCloud = WordCloud(max_words=WC_max_words, mask=mask, background_color='white', colormap='brg', random_state=1)
wordCloud = WordCloud(max_words=WC_max_words, background_color='white', colormap='brg', random_state=1)

wordCloud.generate_from_frequencies(word_dict)

#wordCloud.to_file("benz_wc.png")
#wordCloud.to_file("bmw_wc.png")
#wordCloud.to_file("benz_wc_boring.png")
wordCloud.to_file("bmw_wc_boring.png")
