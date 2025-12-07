import argparse
import numpy as np
import pandas as pd
import random
from collections import deque
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

	DBScan(args.data, args.epsilon, args.minSamples, f"../data/{args.output}")

def DBScan(datafile, eps, minSamp, out=None):
	df = pd.read_csv(datafile)

	coords = df[['Latitude','Longitude']].to_numpy()
	coords_rad = np.radians(coords)
	N = len(coords_rad)

	visited = np.zeros(N, dtype=bool)
	labels  = np.full(N, -1, dtype=int)
	core    = np.zeros(N, dtype=bool)

	tree = BallTree(coords_rad, metric='haversine')
	eps_rad = eps / 6371.0
	neighbors = tree.query_radius(coords_rad, eps_rad)

	# Determine core points
	for i in range(N):
		if len(neighbors[i]) >= minSamp:
			core[i] = True

	cluster_id = 1

	for i in range(N):

		if visited[i]:
			continue

		visited[i] = True

		if not core[i]:
			labels[i] = -1
			continue

		# start new cluster
		labels[i] = cluster_id
		queue = deque(neighbors[i])

		#auxilary structure to efficiently track membership to queue
		in_queue = np.zeros(N, dtype=bool)
		in_queue[neighbors[i]] = True

		while queue:
			pt = queue.popleft()

			if not visited[pt]:
				visited[pt] = True

				if core[pt]:
					pt_neighbors = neighbors[pt]

					# expand cluster
					new_pts = pt_neighbors[~in_queue[pt_neighbors]]
					queue.extend(new_pts)
					in_queue[new_pts] = True

			# assign border points
			if labels[pt] == -1:
				labels[pt] = cluster_id

		cluster_id += 1

	df["Cluster"] = labels
	if out:
		df.to_csv(out, index=False)

	return labels

if __name__ == "__main__":
	main()
