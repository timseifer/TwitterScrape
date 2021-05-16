import csv
from textblob import TextBlob
# from googletrans import Translator
import pandas as pd
import time
from mtranslate import translate

infile = 'united_arab_emirates_clean.csv'


COLS = ['date','person','translation','.polarity','p/n', 'Place']

# translator = Translator()

with open(infile, 'r') as csvfile:
    df = pd.DataFrame(columns=COLS)
    rows = csv.reader(csvfile)
    for row in rows:
        date = row[0]
        user = row[1]
        sentence = row[3]
        place = row[4]
        new_entry = []
        translation = translate(sentence, "en","auto")
        time.sleep(1)
        blob = TextBlob(translation)
        new_entry.append(date)
        new_entry.append(user)
        new_entry.append(translation)
        new_entry.append(blob.sentiment.polarity)
        new_entry.append(blob.sentiment.subjectivity)
        new_entry.append(place)
        print(translation)
        print(blob.sentiment.polarity, blob.sentiment.subjectivity)
        single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
        df = df.append(single_tweet_df, ignore_index=True)  
        df.to_csv('UAE-Sentiment-Translation.csv', columns=COLS,index=False) 
