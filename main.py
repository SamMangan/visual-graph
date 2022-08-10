#from graph import Graph

#g = Graph(True)
#g.draw()

print("hello")
import networkx as nx
import holoviews as hv

G = nx.gnm_random_graph(5,7)

nx.draw(G, nx.spring_layout(G, random_state=100))