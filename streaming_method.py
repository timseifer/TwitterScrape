import tweepy
import config
import json
import pandas as pd  
from urllib3.exceptions import ProtocolError

# authorization tokens
consumer_key = config.api_key
consumer_secret = config.api_secret
access_key = config.access_token
access_secret = config.token_secret


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)
        try:
            data = status._json                      
            # decode the json object from twitter         
            # collect geo-tagged data

            # check if place name is available, in case not the entry is named 
            # 'no place'
            place=""
            try:
                place = data['place']['name'].replace(',', '')
            except TypeError:
                place = 'no place'
            place_type=""

            try:
                place_type = str(data['place']['place_type']).replace(',', '')
            except TypeError:
                place_type = 'na'

            bbx=""
            try:
                bbx = str(data['place']['bounding_box']['coordinates']).replace(',', '')
            except TypeError:
                bbx = 'na'

            # check if coordinates is available, in case not tentry is named 
            # 'no coordinates'
            try:
                coord = str(data['coordinates']['coordinates']).replace(',', '')
            except TypeError:
                coord = 'no coordinates'

            # checks valid location, in case there is not enter named 'no 
            # coordinates'
            try:
                loc = str(data['user']['location']).replace(',', '')
            except TypeError:
                loc = 'no location'       
                print(status)
            # remove any characters that might cause problems with csv encoding
            # write to file of your choice
            with open("united_arab_emirates.csv", "a", encoding='utf-8') as f:
                    f.write("%s,%s,%s,%s,%s,%s\n" % (data['created_at'],str(data['user']['screen_name']).replace(',', ''), coord, str(data['text']).replace(',', '').replace('\n',''), place, bbx))

        except Exception as e:
            print(e)
    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")


if __name__ == "__main__":

    # complete authorization and initialize the API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    with open("united_arab_emirates.csv", "w", encoding='utf-8') as f:
        f.write("date,user,coordinates,text,place,bounding_box\n")
while True:
	try:    
        #enter your bounding box for the target city you want to scrape
		stream.filter(locations=[51.6252,22.6316,56.4263,26.1517])
	except (ProtocolError, AttributeError):
		continue