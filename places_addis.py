
from geopy import geocoders  
import csv
from textblob import TextBlob
# from googletrans import Translator
import pandas as pd
import time
from mtranslate import translate
import re
import socket
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time as time


geolocator = Nominatim(user_agent="https://timseifer.github.io/PW/#/")


infile = 'DATA_FILES/extended-snowballed-out.csv'
#'DATA_FILES/united_arab_emirates_clean.csv'


COLS = ['Latitude', 'Longitude']

# translator = Translator()



def get_lat_long(location):
        try:
                translation = translate(location, "am","auto")
                location_place = geolocator.geocode(translation, exactly_one=True, timeout=60)
                return location_place
        except:
                time.sleep(2)

# def update_file(lat_long, new_entry):


array = {
"Addis Mercato",
"St. George’s Cathedral and Museum",
"Meskel Square and Museums",
"Kidist Selassie",
"National Museum of Ethiopia",
"Ethnological Museum",
"Lion of Judah",
"Derg Monument",
"Entoto Hill",
"Shiro Meda Market",
"Edna Mall and Bole Medhane Alem Cathedral",
"የኢትዮጵያ ብሔራዊ ሙዚየም",
"አዲስ ከተማ",
"Addis Ketema",
"Akaky Kaliti",
"Akaki Kality",
"አራዳ",
"Bole",
"ቦሌ",
"Gullele",
"ጉለሌ",
"Kirkos",
"ቂርቆስ",
"Kolfe Keranio",
"ኮልፌ ቀራንዮ",
"Lideta",
"ልደታ",
"Nifas Silk-Lafto",
"ኒፋስ ሐር-ላፍቶ",
"Yeka",
"የየካ",
"የመርካቶ ገበያ",
"መስቀል አደባባይ",
"የአዲስ አበባ ሙዚየም",
"Addis Ababa Museum",
"Holy Trinity Cathedral",
"ቅድስት ሥላሴ ካቴድራል",
"ሸገር ፓርክ",
"Sheger Park",
"ሾላ ገበያ ዜዶ",
"Bora Amusement Park",
"የቦራ መዝናኛ ፓርክ",
"ቢሄረ ጽጌ የህዝብ መናፈሻ",
"Bihere Tsige Public Park",
"Lafto Park",
"ላፍቶ ፓርክ",
"Washa Mikael Rock Hewn Church",
"ዋሻ ሚካኤል ሮክ ሂው ቤተክርስቲያን"
}


# https://www.geeksforgeeks.org/python-filter-list-of-strings-based-on-the-substring-list/
def Filter(string, substr):
    return [str for str in string if
             any(sub in str for sub in substr)]

with open(infile, 'r') as csvfile:
    df = pd.DataFrame(columns=COLS)
    rows = csv.reader(csvfile)
    for row in rows:
        new_entry = []
        # getting data fields
        try:
            date = row[0]
            user = row[1]
            sentence = row[3]
            place = row[4]
        except:
            continue
        new_entry = []
##################################################
#   Search through text looking for mentions of places in Addis Ababa
#
        for word in array:
            if(sentence.find(word) != -1):
                print("contains the word " + word)
                # print(sentence)
                try:
                    try:
                        lat_long = get_lat_long(word)
                    except:
                        print("unable to find location")
                        continue
                    new_entry.append(lat_long.latitude)
                    new_entry.append(lat_long.longitude)
                    print(lat_long.latitude)
                    print(lat_long.longitude)
                    location_mention = pd.DataFrame([new_entry], columns=COLS)
                    df = df.append(location_mention, ignore_index=True) 
                    df.to_csv('lat_long_regex.csv', columns=COLS,index=False) 
                except Exception as e:
                    print("data frames messed up, dropping last append" + str(e))
                    # df = df[:-1] 
                    continue
            else:
                #if it's not in the sentence look for it in place
                if(place.find(word) != -1):
                    print("contains the word " + word)
                    # print(sentence)
                    try:
                        try:
                            lat_long = get_lat_long(word) 
                        except:
                            print("unable to find location")
                            continue
                        new_entry.append(lat_long.latitude)
                        new_entry.append(lat_long.longitude)
                        location_mention = pd.DataFrame([new_entry], columns=COLS)
                        df = df.append(location_mention, ignore_index=True) 
                        df.to_csv('lat_long_regex.csv', columns=COLS,index=False) 
                    except Exception as e:
                        print("data frames messed up, dropping last append" + str(e))
                        # df = df[:-1]
                        continue

            

        