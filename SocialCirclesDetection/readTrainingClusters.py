import igraph
import sys

def getTrainingClusters(graphFileName, trainingFileName):
	graph = igraph.Graph.Read_Ncol(graphFileName)
	membership = [0] * graph.vcount()
	with  open(trainingFileName, "r") as inputfile:
		i = 0
		for line in inputfile:
			nodes = line.split(":")[1].split(" ")
			for node in nodes:
				for (j, vertex) in zip(range(0, graph.vcount()), graph.vs()):
					if(vertex["name"] == node):
						membership[j] = i
			i = i + 1
	clusters = igraph.clustering.VertexClustering(graph, membership)
	return clusters

if __name__ == "__main__":
	getTrainingClusters(sys.argv[1], sys.argv[2])
