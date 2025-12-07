import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

EPSILON = 500 #km
NEIGHBORHOOD_SIZE = 5

df = pd.read_csv("earthquakes.csv")

# convert degrees to radians for haversine clustering
# euclidian is weird with taking cosine of latitude
radians = np.radians(df[["Latitude", "Longitude"]].values)

db = DBSCAN(EPSILON/6371.0, min_samples=NEIGHBORHOOD_SIZE, metric='haversine')
# give cluster ids or -1 for outliers
df['cluster'] = db.fit_predict(radians)

for cid, group in df.groupby('cluster'):
    if(cid == -1): continue
    print(f"Cluster {cid}: {len(group)} events")

# GEM Global Active Faults Database
# imported from:
# https://github.com/cossatot/gem-global-active-faults/tree/master/geojson
# geojson format, polygon/line shape (non-centroid points)
GEM_GAF_DB = gpd.read_file("fault_lines.geojson")

GEM_GAF_DB['plot_lon'] = GEM_GAF_DB.geometry.centroid.x
GEM_GAF_DB['plot_lat'] = GEM_GAF_DB.geometry.centroid.y

plt.figure(figsize=(12, 6))

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world.boundary.plot(ax=plt.gca(), color='gray', linewidth=0.5, alpha=0.5)

clusters = df['cluster'].unique()
for id in clusters:
    points = df[df['cluster'] == id]
    # outliers
    if id == -1:
        plt.scatter(points["Longitude"], points["Latitude"], color='red', marker='o', s=400, alpha=0.1)
        plt.scatter(points["Longitude"], points["Latitude"], color='red', marker='x', s=20, label='Outliers + affected radius' if id==-1 else "")
    # clusters
    else:
        plt.scatter(points["Longitude"], points["Latitude"], s=10)

# geojson overlay
# form lines from centroids ax
GEM_GAF_DB.plot(ax=plt.gca(), color='black', linewidth=1, label='GEM GAF-DB', alpha=0.7)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"DBSCAN Outliers + Non-Scaled Affected Radii (NEIGHBORHOOD_SIZE = 3)")
plt.legend()
plt.show()

outliers = df[df['cluster'] == -1]
print("\n")
print(f"num_outliers: {len(outliers)}\n")
print(f"Outlier Average Magnitude = {np.mean(outliers['Magnitude'])}")
print(f"Outlier Median Magnitude = {np.median(outliers['Magnitude'])}\n")
