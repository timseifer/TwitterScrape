# TwitterScrape

Twitter Scrape utilizes a series of scripts to manipulate Twitter Geo-Tagged JSON data into CSV files

## Description

There are two methods to scraping geo-tagged tweets: One involves streaming tweets with a bounding box and the other is point radius method. The scripts can be identified as streaming_method.py & geo_locator.py respectively.

The streaming bounding box method can continuously run on an AWS server.

The general running of data should be as follows:
streaming_method.py -> your_data.csv -> snowball_data.py -> your_data_larger.csv

After you have your_data.csv or your_data_larger.csv run them through auxillary scripts:
your_data.csv -> sentiment_analysis.py -> your_data_sentiment.csv

To map data, specify the espg in map_data.py and run the following:
your_data.csv -> just_coordinates.py -> your_coordinates.csv -> map_data.py -> Map of geo-location and tweet coordinates


### Executing program

python3 (streaming_method.py or snowball_data.py, or any others depending on the stage of data anlysis) 

Change the script names within python files for the data you are working on.
