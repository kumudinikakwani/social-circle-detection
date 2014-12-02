import igraph
import sys
from collections import Counter
from readTrainingClusters import getTrainingClusters
import random

featureNames = []


def getSimilarity(node1, node2):
	similarity = 0
	
	# Calculate profile similarity
	for featureName in featureNames:
		if(node1[featureName] == node2[featureName]):
			similarity = similarity + 1

	
	# Calculate number of common neigbours
	similarity = similarity + len(list(set(graph.neighborhood(node1.index)) & set(graph.neighborhood(node2.index))))
	
	# Is there an edge between the two?
	if node1.index in graph.neighbors(node2):
		similarity = similarity + 1	
	return similarity

		
def findNewCentroid(nodes):
	similarities = [0] * len(nodes)
	for i,node1 in zip(range(0,len(nodes)),nodes):
		for node2 in nodes:
			similarities[i] = similarities[i] + getSimilarity(node1, node2)
	
	max = similarities[0]
	index = 0
	for i in range(0,len(nodes)):
		if max < similarities[i]:
			max = similarities[i]
			index = i
	return nodes[index]	
	

# Nodes should be a list of list of nodes in all the centroids
def findNewCentroids(nodes):
	centroids = []
	for nodesList in nodes:
		centroids.append(findNewCentroid(nodesList))
	return centroids


def getNearestCentroid(node, centroids):
	maxSimilarity = 0
	nearestCentroid = centroids[0]
	for centroid in centroids:
		temp = getSimilarity(node, centroid)
		if(temp > maxSimilarity):
			maxSimilarity = temp
			nearestCentroid = centroid
	return nearestCentroid
	
		
def getAllNearestCentroids(nodes, centroids):
	nearestCentroids = []
	for node in nodes:
		nearestCentroid = getNearestCentroid(node, centroids)
		nearestCentroids.append(nearestCentroid)
	return nearestCentroids



def kmeans(graph, k):
	
	# Pick random nodes initially
	centroids = [0] * k
	for i in range(0,k):
		randomNode = graph.vs[random.randrange(0, graph.vcount())]
		while(randomNode in centroids):
			randomNode = graph.vs[random.randrange(0, graph.vcount())]
		centroids[i] = randomNode

	newCentroids = [graph.vs[0]] * k
	
	
	iterations = 0
	# while centroids don't change
	while(cmp(newCentroids, centroids) != 0 and iterations < 20):
		nodesListOfLists = []
		nearestCentroids = getAllNearestCentroids(graph.vs, centroids)
		if iterations > 0:
			centroids = newCentroids
		newCentroids = set(nearestCentroids)
		
		for i,newCentroid in zip(range(0,k),newCentroids):
			temp = []
			for node in graph.vs:
				if nearestCentroids[node.index] == newCentroid:
					temp.append(node)
					node['membership'] = i
			nodesListOfLists.append(temp)
		print len(newCentroids)
		print len(nearestCentroids)
		print len(nodesListOfLists)
		newCentroids = findNewCentroids(nodesListOfLists)
		iterations = iterations + 1
	
	clusters = igraph.VertexClustering(graph, membership=graph.vs['membership'])	
	
	return clusters		 		


def main(graphFileName, featuresFileName, featureListFile, trainingFileName, k):

	# Read ego network
	global graph
	graph = igraph.Graph.Read_Ncol(graphFileName)
	graph.vs["membership"] = 0

	# Read feature names	
	with open(featureListFile, "r") as featureList:
		for line in featureList:
			featureNames.append(line.strip())
			graph.vs[line.strip()] = None
				
	
	# Read feature values of nodes
	with open(featuresFileName, "r") as featuresFile: 
		for line in featuresFile:
			features = line.split(" ")	
			for feature in features[1:-1]:
				try:
					node = graph.vs[int(features[0])]
					node[";".join(feature.split(";")[0:-1])] = feature.split(";")[-1]
				except:
					pass
			
			
	
	# Run K-Means on the graph
	clusters = kmeans(graph, k)
	newClusters = clusters
	
	# Store in each node the cluster it belongs to.
	i = 0
	for membership in clusters.membership:
		graph.vs[i]['membership'] = membership
		i = i + 1
	
	
	# Plot final clusters
	print newClusters
	igraph.plot(newClusters)
	
	# Plot actual clusters from training data
	actualClusters = getTrainingClusters(graphFileName, trainingFileName)
	print actualClusters
	igraph.plot(actualClusters)

	i = 0
	count = 0
	for node1 in graph.vs:
		for node2 in graph.vs:
			if(actualClusters.membership[node1.index] == actualClusters.membership[node2.index] and newClusters.membership[node1.index] == newClusters.membership[node2.index]):
				count = count + 1
			elif(actualClusters.membership[node1.index] != actualClusters.membership[node2.index] and newClusters.membership[node1.index] != newClusters.membership[node2.index]):
				count = count + 1
			i = i + 1
	error = (float(count) / float(i))
	print error
	




"""
 Usage: python main.py <graph file name> <features file name> <features list file name> <training circles file name>
"""
if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]))
