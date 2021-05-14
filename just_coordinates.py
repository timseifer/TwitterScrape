
#!/usr/bin/env python3
"""
Latitude and longitude from either a geo-tagged coordinate or based on the 
place the user lives.
"""

import csv
import pandas as pd
import re
from geopy.geocoders import Nominatim

infile = 'united_arab_emirates_clean.csv'

#set to a random website so the API allows you acess

geolocator = Nominatim(user_agent="https://timseifer.github.io/PW/#/")

COLS = ['Latitude','Longitude']

with open(infile, 'r') as csvfile:
    df = pd.DataFrame(columns=COLS)
    rows = csv.reader(csvfile)
    for row in rows:
        new_entry = []
        coordinates = row[2]
        if (coordinates == 'no coordinates' or coordinates == 'coordinates' or coordinates == '' or len(coordinates) > 50):
            location = geolocator.geocode(row[4])
            # if  alocation exists then enter it's respective geo coordinates
            # to the file
            if(location is not None):
                print(location.latitude)
                print(location.longitude)
                new_entry.append(location.latitude)
                new_entry.append(location.longitude)
                single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
                df = df.append(single_tweet_df, ignore_index=True)  
            continue
        else:
            # parsing data so it's clean for further analysis in map_data
           lhs, rhs = coordinates.split(" ", 1)
           lhs = re.sub('[[]', '', lhs)
           rhs = re.sub('[]]', '', rhs)
           print(lhs)
           print(rhs)
        new_entry.append(lhs)
        new_entry.append(rhs)
        single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
        df = df.append(single_tweet_df, ignore_index=True)  
        df.to_csv('lat_long.csv', columns=COLS,index=False) 