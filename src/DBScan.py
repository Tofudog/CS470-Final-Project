import argparse
import numpy as np
import pandas as pd
import haversine as hs
import random


#this program takes a file and uses DBScan algorithm to cluster around latitudinal and longitudinal data
def main():

	# set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data",
                        default="../data/earthquakes.csv",
                        help="filename for data")
    parser.add_argument("-e", "--epsilon",
    					type=int,
                        default=500,
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

    #define a cluster column, initializing each row as an outlier
    df["Cluster"] = -1

    #define an empty set for checked points 
    checkedPts = set()

    #define a set that contains the index of each unchecked point (at start, all points)
    uncheckedPts = set(df.index.tolist())

    #start cluster counter at 1
    curCluster = 1
    neighborhood = set()
    curPoint = uncheckedPts.pop()

    while(len(uncheckedPts) != 0):
	    #choose a point to begin DBScan algorithm


	    if curPoint in checkedPts: #point has been checked before
	    	#make sure they aren't still in unchecked list
    		uncheckedPts.discard(curPoint)

    		#set to check next point in neighborhood
	    	if len(neighborhood != 0):
	    		curPoint = neighborhood.pop()
	    		continue

	    	#neighborhood is empty, select any new point to continue
	    	curPoint = uncheckedPts.pop()

	    checkedPts.add(curPoint)

	    for i in range(numRows):
	    	if(i <)

    print(df)


if __name__ == "__main__":
    main()
