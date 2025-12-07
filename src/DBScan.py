import argparse
import numpy as np
import pandas as pd
import haversine as hs
import random
from sklearn.neighbors import BallTree


#this program takes a file and uses DBScan algorithm to cluster around latitudinal and longitudinal data
def main():

	# set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data",
                        default="../data/earthquakes.csv",
                        help="filename for data")
    parser.add_argument("-e", "--epsilon",
    					type=float,
                        default=500.0,
                        help="neighborhood radius (in km)")
    parser.add_argument("-m", "--minSamples",
    					type=int,
                        default=5,
                        help="minimum number of samples to trigger extension of cluster")
    parser.add_argument('-o', '--output',
                        help="file to store output of clustering in")
    
    args = parser.parse_args()

    DBScan(args.data, args.epsilon, args.minSamples, args.output)

#REF: distance_km 	 = hs.haversine(loc1, loc2)
#	  distance_miles = hs.haversine(loc1, loc2, unit=hs.Unit.MILES)

def DBScan(datafile, eps, minSamp, out):
    # load the dataset
    df = pd.read_csv(datafile, index_col=False)
    numRows = len(df)

    #define tuple (Latitude, Longitude) for each entry in dataset
    df["Location"] = df[['Latitude', 'Longitude']].apply(tuple, axis=1)
    df = df.drop(["Latitude", 'Longitude'], axis=1)

    #shuffle dataset, to avoid always classify border points the same way
    df = df.sample(frac=1)
    df = df.reset_index(drop=False) #reset indices

    #define a cluster column, initializing each row as an outlier
    df["Cluster"] = -1

    #convert longitude/latitude from degrees to radians
    locs = np.array(df["Location"])
    locs_rad = np.radians(locs)

    #build a BallTree to efficiently find neighbors
    tree = BallTree(locs_rad, metric='haversine')

    #convert eps into radians (km = radians * earth-radius)
    eps_rad = eps / 6,371

    #get neighbors for each point
    neighbors = tree.query_radius(locs_rad, r=eps_rad)

    #define a dictionary for points to tell if we visited them
    visited = {pointIndex: False for pointIndex in df.index.tolist()}

    #start cluster counter at 1
    curCluster = 1

    for i in visited:

    	#skip already visited points
    	if visited[i]: continue 

    	#mark current point as visited
    	visited[i] = True

    	nHood = list(neighbors[i])

    	#leave points with unpopulated neighborhoods unchanged
    	if(len(nHood) < minSamp): continue

    	#we have a cluster!
    	df.iloc[i]["Cluster"] = curCluster

    	neighbor_stack = nHood

    	while neighbor_stack:
    		i = stack.pop()

    		if not visited[i]:
    			visited[i] = True
    			nHood = list(neighbors[i])

    			if len(nHood) >= minSamp:
    				neighbor_stack.extend(nHood)

    		df.iloc[i]["Cluster"] = curCluster

    	curCluster += 1

    print(f"Algorithm Complete, outputting to {out}")

    #resort as it was before, drop indices, and save
    df = df.sort_values(by='index')
    df = df.drop(['index'], axis=1)

    df.to_csv(out, index=False)

    return df["Cluster"]


if __name__ == "__main__":
    main()
