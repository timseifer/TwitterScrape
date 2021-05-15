
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


df = pd.read_csv("lat_long.csv", delimiter=',', skiprows=0, low_memory=False)
df['coords'] = list(zip(df['Longitude'], df['Latitude']))
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

# gdf = GeoDataFrame(df, geometry=geometry)   

geo_df = gpd.GeoDataFrame(
    df,
    geometry = geometry,
)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
base = world[(world.name == "United Arab Emirates")].plot(color='white', edgecolor='black')
geo_df.clip(world, base)
geo_df.plot(ax=base, marker='o', color='red', markersize=1).clip()
# gdf.plot(color='none',edgecolor='green', ax = ax)
plt.show()
