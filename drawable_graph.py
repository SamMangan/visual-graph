import matplotlib.pyplot as plt
import networkx as nx


class DrawableGraph:
  
  class Node:
    def __init__(self, value, graph):
      self.value = value
      self._graph = graph

    def __repr__(self):
      return f"Node({self.value})"

    @property
    def colour(self):
      ret = self._graph.colours.get(self.value)
      return ret
      #return self._graph.colours.get(self.value)

    @colour.setter
    def colour(self, colour):
      self._graph.colours = {self.value:colour}

    @property
    def neighbours(self):
      return [self._graph._nodes[neighbour] for neighbour in self._graph._graph.neighbors(self.value)]
      
  def __init__(self, nodes, edges):
    #self._graph = nx.gnm_random_graph(nodes, edges)
    self._graph = nx.bipartite.gnmk_random_graph(nodes, nodes, edges)
    self._nodes = [DrawableGraph.Node(value, self) for value in self._graph.nodes] 
    
    self._pos = nx.spring_layout(self._graph)
    plt.figure().set_figwidth(4.5)

  def _get_attributes(self, name):
    nx_attributes =  nx.get_node_attributes(self._graph, name)
    return {node.value:nx_attributes.get(node.value) for node in self.nodes}

  def _set_attributes(self, name, attributes):
    nx.set_node_attributes(self._graph, attributes, name=name)

  @property
  def nodes(self):
    return self._nodes

  @property
  def colours(self):
    return self._get_attributes("colour") 

  @colours.setter
  def colours(self, value):
    self._set_attributes("colour", value)

  def draw(self):
    colours = [colour if colour else "white" for colour in self.colours.values()]
    nx.draw(self._graph, self._pos, with_labels=True, node_color=colours, edgecolors="black")

  def update_drawing(self, pause=1):
    self.draw()
    plt.pause(pause)

  def show(self):
    plt.show(block=False)