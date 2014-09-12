import igraph
import sys
from readTrainingClusters import getTrainingClusters


"""
Create clusters using various community detection methods, returns the
actual clusters read from training file along with different sets of clusters
obtained using different methods.
"""
def compare(graphFileName, trainingFileName):
	graph = igraph.Graph.Read_Ncol(graphFileName)
	clustersList = []
	actualClusters = getTrainingClusters(graphFileName, trainingFileName)
	clustersList.append(graph.as_undirected().community_multilevel())
	clustersList.append(graph.community_edge_betweenness())
	#clustersList.append(graph.community_optimal_modularity())
	clustersList.append(graph.community_label_propagation())
	#clustersList.append(graph.as_undirected().community_fastgreedy())
	clustersList.append(graph.community_infomap())
	clustersList.append(graph.as_undirected().community_leading_eigenvector())
	return (actualClusters, clustersList)



"""
Usage: python compareCommunityDetectionMethods.py <egonet file in edgelist format> <training circle file for the egonet>
TODO: Can we plot all the clusters in one output file on different pages?
"""
if __name__ == "__main__":
	actualClusters, clustersList  = compare(sys.argv[1], sys.argv[2])
	igraph.plot(actualClusters)
	for clusters in clustersList:
		igraph.plot(clusters)
