
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

# used pandas to extract data from the csv file.

df = pd.read_csv("lat_long.csv", delimiter=',', skiprows=0, low_memory=False)
df['coords'] = list(zip(df['Longitude'], df['Latitude']))
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

gdf = GeoDataFrame(df, geometry=geometry)   

geo_df = gpd.GeoDataFrame(
    df,
    geometry = geometry
)

# utilize epsg and stamen tiles api to set background image.

geo_df.set_crs(3857, allow_override=True, inplace=True)
ax = geo_df.to_crs(epsg=27040).plot(edgecolor="red", 
                                       facecolor="none",  
                                       linewidth=2,
                                       figsize=(9, 9))
ctx.add_basemap(ax, zoom='auto')
ax.set_axis_off()

# show the plot that was created.
plt.show()
