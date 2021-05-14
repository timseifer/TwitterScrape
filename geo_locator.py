#!/usr/bin/env python3
"""
A scraper for locations based on latitude, longitude, and radius
for twitter. 

A recent method that was tested using circle radius' on individual cities
"""

import config
import tweepy
import pandas as pd
import json
from translate import Translator
#hiding api keys
auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


#Create list for column names
COLS = ['id','created_at','lang','original text','user_name', 'place', 'place type', 'bbx', 'coordinates', 'location', 'geo_enabled', 'parsed from query']
geo='8.9806,38.7578,50km'
since_date='202103082000'
until_date='202104070000'
max_pages = 500
#The Twitter Search API searches against a sampling of recent Tweets published 
# in the past 7 days. 
def write_tweets(all_words):
    df = pd.DataFrame(columns=COLS)
    for word in all_words:
    # iterate through pages with given condition
    # using tweepy.Cursor object with items() method

        for page in tweepy.Cursor(api.search, q=word, include_rts=True,
                    fromDate = since_date, toDate= until_date).pages(1000):
                        for tweet in page:

                            #creating string array
                            new_entry = []

                            #storing all JSON data from twitter API
                            tweet = tweet._json 
                            print(tweet)

                            # Append the JSON parsed data to the string list:
                            new_entry += [tweet['id'], tweet['created_at'], tweet['lang'], tweet['text'], 
                                        tweet['user']['name']]

                            #check if place name is available, in case not the entry is named 'no place'
                            place=""
                            try:
                                place = tweet['place']['full_name']
                            except TypeError:
                                place = 'no place'
                            new_entry.append(place)
                            place_type=""
                            try:
                                place_type = tweet['place']['place_type']
                            except TypeError:
                                place_type = 'na'
                            new_entry.append(place_type)
                            bbx=""
                            try:
                                bbx = tweet['place']['bounding_box']['coordinates']
                            except TypeError:
                                bbx = 'na'
                            new_entry.append(bbx)

                            #check if coordinates is available, in case not the entry is named 'no coordinates'
                            try:
                                coord = tweet['coordinates']['coordinates']
                            except TypeError:
                                coord = 'no coordinates'
                            new_entry.append(coord)

                            #check if location is available, in case not the entry is named 'no coordinates'
                            try:
                                loc = tweet['user']['location']
                            except TypeError:
                                loc = 'no location'
                            new_entry.append(loc)

                            new_entry.append(tweet['user']['geo_enabled'])
                            new_entry.append(word)
                            
                            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
                            df = df.append(single_tweet_df, ignore_index=True)
                            
        df.to_csv('tweets_from_addis_ababa.csv', columns=COLS,index=False)




#declare keywords as a query
keyword_en=[]

# grabbing all tweets because we are getting a very low yield
#1 minute, or mile left or right is approximatley .01666, adding this value 
# decrements or increases our mileage by 1.15, so approximatley .02 will 
# increase by two miles

write_tweets(["geocode:8.972140,38.757004,1mi", "geocode:9.0006,38.7578,1mi","geocode:9.0806,38.7578,1mi","geocode:9.0806,38.7778,1mi", "geocode:9.000832,38.779685,1mi", "geocode:9.000132,38.779685,1mi", "geocode:9.0169988,38.856412,1mi", "geocode:9.042597,38.835305,1mi", "geocode:9.075145,38.894331,1mi","geocode:8.878966,38.80207,1mi", "geocode:8.95935,38.675655,1mi","geocode:8.93137,38.657616,1mi", "geocode:9.003769,38.729252,1mi", "geocode:8.9821522,38.72770,1mi","geocode:8.9577842, 38.7237388,1mi", "geocode:9.02870382,38.734374,1mi","geocode:9.03152,38.75798,1mi", "geocode:9.026774,38.786614,1mi", "geocode:8.943398,38.749192,1mi", "geocode:8.999521,38.698208,1mi", "geocode:9.057161,38.732026,1mi", "geocode:9.006811,38.810304,1mi", "geocode:9.055974,38.761295,1mi","geocode:9.012745,38.839572,1mi", "geocode:9.029190,38.704732,1mi", 
"geocode:9.035293,38.811162,1mi", "geocode:9.055466,38.790649,1mi", "geocode:9.014100,38.869956,1mi", "geocode:9.041735,38.865750,1mi", "geocode:8.988161,38.853047,1mi", "geocode:8.971545,38.699925,1mi","geocode:8.893283,38.776572,1mi","geocode:8.900011,38.813862,1mi", "geocode:8.917198,38.737775,1mi", "geocode:8.932206,38.712284,1mi", "geocode:8.988161,38.672116,1mi", "geocode:9.015966,38.677609,1mi","geocode:9.057331,38.703530,1mi", "geocode:9.006557,38.897422,1mi", "geocode:8.953843,38.779170,1mi", "geocode:9.006557,38.897422,1mi", "geocode:9.070044,38.865407,1mi", "geocode:8.948398,38.697608,1mi", "geocode:8.857753,38.781636,1mi"])

# Excuse the incredibly large hyperlink, shows the circle method


#https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B1609.34%2C9.0423835%2C38.8356258%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0423835%2C38.8356258%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9721396%2C38.7570037%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0006493%2C38.757788%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.080069%2C38.7571444%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.079383%2C38.7751293%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9998685%2C38.7798549%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0423835%2C38.8356258%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0749751%2C38.8941113%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.879021%2C38.80219%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9594815%2C38.6757786%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9310352%2C38.6566497%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0047882%2C38.729737%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9817533%2C38.7271763%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9577599%2C38.7237373%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0286882%2C38.7342598%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0318512%2C38.7580149%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0267736%2C38.7866144%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.943398%2C38.7491917%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.999521%2C38.6982083%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0571607%2C38.7320263%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.006811%2C38.8103035%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0559742%2C38.7612946%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.012745%2C38.8395718%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0291896%2C38.7047319%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0352926%2C38.811162%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0554655%2C38.7906486%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0141003%2C38.8699562%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0417345%2C38.8657503%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.988161%2C38.8530472%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9605283%2C38.809498%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.971545%2C38.6999248%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.8932832%2C38.7765719%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9227094%2C38.7692755%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9000111%2C38.8138618%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.917198%2C38.7377754%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9322055%2C38.7122843%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9881611%2C38.6721157%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.015966%2C38.6776094%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0573306%2C38.7035303%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0065573%2C38.8974217%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.9538431%2C38.7791697%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C9.0700441%2C38.8654071%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1609.34%2C8.948398%2C38.697608%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1684.83%2C8.8577531%2C38.7816355%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D