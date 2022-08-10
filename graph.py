import random
import time

import networkx as nx

# matplotlib imports super slow for some reason ... TODO investigate
print("importing matplotlib...")
start = time.time()
import matplotlib.pyplot as plt
print(f"done importing matplotlib (took {time.time()-start:.1f} seconds)...")

COLOUR_1 = "mediumpurple"
COLOUR_2 = "goldenrod"

class Graph:
  def __init__(self, populate=False):
    if populate:
      self._graph = nx.gnm_random_graph(5,7)
    else:
      self._graph = nx.Graph()
      
  def draw(self, width=4.5):
    plt.figure().set_figwidth(width)
    print("drawing graph...")
    colours = random.choices([COLOUR_1, COLOUR_2], k=5)
    nx.draw(self._graph, with_labels=True, font_weight="bold", node_color=colours)
    print("displaying graph...")
    plt.show(block=False)


# from collections import defaultdict
# class Graph:
#   def __init__(self):
#     self._adjacency_list = defaultdict(set) # maps nodes to sets of connected nodes

#   def __str__(self):
#     return "\n".join([f"{node}->({','.join([node for node in nodes])})" for node, nodes in self._adjacency_list.items()])
  
#   def add(self, node1, node2):
#     self._adjacency_list[node1].add(node2)
#     self._adjacency_list[node2].add(node1)
