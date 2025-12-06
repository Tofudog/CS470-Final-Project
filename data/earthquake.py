import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

radius = 500
neighborhood_size = 3

df = pd.read_csv("earthquakes.csv")

# convert degrees to radians for haversine clustering
# euclidian is weird with taking cosine of latitude
radians = np.radians(df[["Latitude", "Longitude"]].values)

db = DBSCAN(radius/6371.0, min_samples=neighborhood_size, metric='haversine')
# give cluster ids or -1 for outliers
df['cluster'] = db.fit_predict(radians)


# GEM Global Active Faults Database
# imported from:
# https://github.com/cossatot/gem-global-active-faults/tree/master/geojson
# geojson format, polygon/line shape (non-centroid points)
GEM_GAF_DB = gpd.read_file("fault_lines.geojson")

GEM_GAF_DB['plot_lon'] = GEM_GAF_DB.geometry.centroid.x
GEM_GAF_DB['plot_lat'] = GEM_GAF_DB.geometry.centroid.y

plt.figure(figsize=(12, 6))

clusters = df['cluster'].unique()
for id in clusters:
    points = df[df['cluster'] == id]
    # outliers
    if id == -1:
        plt.scatter(points["Longitude"], points["Latitude"],
                    color='red', marker='x', s=10, label='Outliers' if id==-1 else "")
    # clusters
    else:
        plt.scatter(points["Longitude"], points["Latitude"],
                    s=10)

# geojson overlay
# form lines from centroids ax
GEM_GAF_DB.plot(ax=plt.gca(), color='black', linewidth=1, label='GEM GAF-DB')

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"dbscan - fault lines overlayed")
#plt.legend()
plt.show()

outliers = df[df['cluster'] == -1]
print(f"num_outliers: {len(outliers)}\n")
print(outliers[["Latitude", "Longitude", 'Magnitude']])
