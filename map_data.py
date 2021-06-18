
#!/usr/bin/env python3
"""
Map the data from a latitude, longitude csv file using Contextily utilizing
epsg for higher levels of data extraction.
"""

__author__ = "Tim Seifert"
__license__ = "N/A"


import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import contextily as ctx
import folium
# from folium.plugins import Map
import webbrowser
filepath = '/Users/timseifert/Desktop/Twitter Scraping/map_reg.html'

mapit = folium.Map(location=[23.4241, 53.8478], zoom_start = 13) 
df = pd.read_csv("lat_long_UAE_v2_correct.csv", delimiter=',', skiprows=0, low_memory=False)
map_data = list(zip(df['Longitude'], df['Latitude']))
for coord in map_data:
    folium.Marker(location=[coord[0], coord[1]], fill_color='#43d9de', radius=1 ).add_to( mapit)

mapit.save(filepath)
webbrowser.open('file://' + filepath)

# geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

# # gdf = GeoDataFrame(df, geometry=geometry)   

# geo_df = gpd.GeoDataFrame(
#     df,
#     geometry = geometry,
# )

# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# base = world.plot(color='white', edgecolor='black', cmap='OrRd')
# # geo_df.clip(world, base)
# geo_df.plot(ax=base, marker='o', color='red', markersize=1)
# # gdf.plot(color='none',edgecolor='green', ax = ax)
# plt.show()
