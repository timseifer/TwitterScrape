#!/usr/bin/env python3
"""
Garner sentiment analysis from a CSV file
"""

import csv
from textblob import TextBlob
from googletrans import Translator
import pandas as pd

# the file you are running the sentiment analysis on
infile = 'united_arab_emirates_clean.csv'

COLS = ['date','person','translation','.polarity','p/n', 'Place']

translator = Translator()

with open(infile, 'r') as csvfile:
    df = pd.DataFrame(columns=COLS)
    rows = csv.reader(csvfile)
    for row in rows:

        # change according to where the data is located in the CSV file
        date = row[0]
        user = row[1]
        sentence = row[3]
        place = row[4]
        new_entry = []
        
        # auto translate to english
        blob = TextBlob(translator.translate(sentence).text)
        new_entry.append(date)
        new_entry.append(user)
        new_entry.append(translator.translate(sentence).text)
        new_entry.append(blob.sentiment.polarity)
        new_entry.append(blob.sentiment.subjectivity)
        new_entry.append(place)

        #debugging, assuring translation occurs
        print(translator.translate(sentence).text)

        # assure the sentiment is printing correctly
        print(blob.sentiment.polarity, blob.sentiment.subjectivity)

        #append data_fram
        sentiment_df = pd.DataFrame([new_entry], columns=COLS)
        df = df.append(sentiment_df, ignore_index=True)

        # rename to csv file of your choice
        df.to_csv('UAE-Sentiment-Translation.csv', columns=COLS,index=False) 
