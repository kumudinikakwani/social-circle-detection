from adjlist_to_edgelist import convert
import igraph

convert("../../Data/egonets/239.egonet")
graph = igraph.load("../../Data/egonets/239.egonet.edgelist", format="edgelist")
igraph.plot(graph)
