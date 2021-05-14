#!/usr/bin/env python3
"""
Snowball_Data takes unique user_ids and scrapes home profiles 
for historical data
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
COLS = ['id','created_at','lang','original text','user_name', 'place', 'place type', 'bbx', 'coordinates', 'location', 'geo_enabled', 'parsed_from']


from csv import reader

# If a crash occurs utilize the below code from 28-39 to pick up
# where you left off. ps -x can sometimes be rude.

# open file in read mode
already_populated = []
with open('extended-snowballed-out-other-half.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
	for row in csv_reader:
		try:
			if row[12] not in already_populated:
				if row[12] != "parsed_from":
					print(row[12])
					already_populated.append(row[12])
		except:
			pass

# If a crash doesn't occur remove the second portion of line 50
print("**************************")
csv_arr = []
with open('out_clean.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
	for row in csv_reader:
		try:
			if row[1] not in csv_arr and row[1] not in already_populated:
				if row[1] != "user":
					print(row[1])
					csv_arr.append(row[1])
		except:
			pass
print("**************************")


# write tweets utilizes the twitter api and a list of usernames to 
# gather tweets from people's home timelines

def write_tweets(all_usernames):
	# create dataframe from defined column list
	df = pd.DataFrame(columns=COLS)	
	for user_name in all_usernames:
	# iterate through pages with given condition
	# using tweepy.Cursor object with items() method

		print("*********RUNNING USERNAME***********")
		print(user_name)
		# good = True
		try:
			for page in tweepy.Cursor(api.user_timeline, screen_name=user_name, tweet_mode="extended").pages(100):
							# if good != True:
							# 	break
							for tweet in page:
								#creating string array
								new_entry = []

								#storing all JSON data from twitter API
								tweet = tweet._json 
								#make use of the translator
								#Append the JSON parsed data to the string list:
								loc = ""
								try:
									loc = tweet['user']['location']
								except TypeError:
									loc = 'no location'
								
								# Comment in if you want to reduce
								# time complexity for only geo-tagged locations
								# if loc not in valid_locations:
								# 	print("location not in selected entries\n")
								# 	print(loc+"\n")
								# 	good = False
								# 	break
								
								new_entry += [tweet['id'], tweet['created_at'],
								 tweet['lang'], tweet['full_text'], 
											tweet['user']['name']]

								# check if place name is available, in case not
								# the entry is named 'no place'

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

								new_entry.append(loc)
								new_entry.append(tweet['user']['geo_enabled'])
								new_entry.append(user_name)
								single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
								df = df.append(single_tweet_df, ignore_index=True)                  
			df.to_csv('crash_after.csv', columns=COLS,index=False)
		except:
			pass
		
write_tweets(csv_arr)
