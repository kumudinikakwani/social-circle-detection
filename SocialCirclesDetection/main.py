import igraph
import sys
from collections import Counter
from readTrainingClusters import getTrainingClusters

def main(graphFileName, featuresFileName, featureListFile, trainingFileName):
	

	# Read ego network
	graph = igraph.Graph.Read_Ncol(graphFileName)

	# Read feature names	
	featureNames = []
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
			
			
	# Clustering
	clusters = graph.community_infomap()
	
	# Store in each node the cluster it belongs to.
	i = 0
	for membership in clusters.membership:
		graph.vs[i]['membership'] = membership
		i = i + 1
	
	# Iteratively refine clusters.
	igraph.plot(clusters)
	parameters = calculateParameters(graph, clusters, featureNames)
	newClusters = refineClusters(graph, parameters)
	while clusterDifference(clusters, newClusters) == True:
		parameters = calculateParameters(graph, newClusters, featureNames)
		clusters = newClusters
		newClusters = refineClusters(graph, parameters)
	
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
	
	

# Calculate parameters of clusters. 
def calculateParameters(graph, clusters, featureNames):
	
	i = 0
	parameters = [None] * len(clusters)
	for cluster in clusters:
		nodes = [node for node in graph.vs if node['membership'] == i]
		parameters[i] = {}
		for feature in featureNames:
			parameters[i][feature] = findMajority([node[feature] for node in nodes], 4 *  len(cluster) / 7)
			 
		i = i + 1
	return parameters

def findMajority(_list, threshold):
	c = Counter(_list)
	if len(c.most_common()) > 0:
		value, count = c.most_common()[0]
		if(count >= threshold):
			return value
		else:
			return None
	else:
		return None

def refineClusters(graph, parameters):
	i = 0
	for parameter in parameters:
		for node in graph.vs:
			if checkParameters(node, parameter) == True:
				node['membership'] = i
		i = i + 1
	clusters = igraph.VertexClustering(graph, membership=graph.vs['membership'])
	return clusters


def checkParameters(node, parameter):
	result = True
	for key, value in parameter.iteritems():
		if value != None and node[key] != value:
				result = False
	return result

def clusterDifference(clustering1, clustering2):
	membership1 = clustering1.membership
	membership2 = clustering2.membership
	result = False
	count = 0
	for member1, member2 in zip(membership1, membership2):
		if member1 != member2:
			count = count + 1
	if count > 5:
		result = True
	return result
"""
 Usage: python main.py <graph file name> <features file name> <features list file name> <training circles file name>
"""
if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
