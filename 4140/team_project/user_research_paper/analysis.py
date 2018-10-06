import pandas as pd
import numpy as np
import nltk

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

df1 = pd.read_csv('./interview1.csv')

app1 = df1['app'].tolist()
mental_health1 = df1['mental_health'].tolist()

app1_sum = 0
for sentence in app1:
	app1_sum += analyzer.polarity_scores(sentence)['compound']


mhealth1_sum = 0
for sentence in mental_health1:
	mhealth1_sum += analyzer.polarity_scores(sentence)['compound']
	
print("Interview 1")
print("app_avg = {}".format(app1_sum/len(app1)))
print("mental_health_avg = {}\n".format(mhealth1_sum/len(mental_health1)))


df2 = pd.read_csv('./interview2.csv')

app2 = df2['app'].tolist()
mental_health2 = df2['mental_health'].tolist()

app2_sum = 0
for sentence in app2:
	app2_sum += analyzer.polarity_scores(sentence)['compound']
	
mhealth2_sum = 0
for sentence in mental_health2:
	mhealth2_sum += analyzer.polarity_scores(sentence)['compound']
	
print("Interview 2")
print("app_avg = {}".format(app2_sum/len(app2)))
print("mental_health_avg = {}\n".format(mhealth2_sum/len(mental_health2)))
