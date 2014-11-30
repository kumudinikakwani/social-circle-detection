import igraph
import sys
import csv
from itertools import izip



graph = igraph.Graph.Read_Ncol(sys.argv[1])
igraph.plot(graph)

# calculate dendrogram
dendrogram = graph.community_edge_betweenness()
# convert it into a flat clustering
clusters = dendrogram.as_clustering()
# get the membership vector
membership = clusters.membership

#Now we can start writing the membership vector along with the node names into a CSV file::
writer = csv.writer(open("output.csv", "wb"))
for name, membership in izip(graph.vs["name"], membership):
    writer.writerow([name, membership])

print graph
print graph["239"]
