import matplotlib.pyplot as plt
import networkx as nx
import random

class DrawableGraph:
  """
  A graph with nodes and edges which can be drawn.
  """
  
  class Node:
    """
    A node containing a value and belonging to a graph.
    """
    def __init__(self, value, graph):
      """
      Parameters
      ----------
      value : int
          The value of the Node
      graph : DrawableGraph
          The graph the Node belongs to
      """
      self.value = value
      self._graph = graph

    def __repr__(self):
      return f"Node({self.value})"

    @property
    def colour(self):
      """string representing the colour of this Node"""
      return self._graph.colours.get(self.value)

    @colour.setter
    def colour(self, colour):
      self._graph.colours = {self.value:colour}

    @property
    def neighbours(self):
      """list of Nodes neigbouring this Node in the graph"""
      nx_neighbours = self._graph._graph.neighbors(self.value)
      return [self._graph._nodes[neighbour] for neighbour in nx_neighbours]

  def _connected_bipartite_graph(n, m, k):
    graph = None
    #print(f"Creating a bipartite graph with {n} nodes in one set, {m} nodes in the other set, and {k} edges")
    while True:
      graph = nx.bipartite.gnmk_random_graph(n, m, k)
      if nx.is_connected(graph):
        break
      #print("Graph was not connected, trying again")
    #print("Done")
    return graph
  
  def __init__(self, nodes, height=4, width=None):
    """
    Parameters
    ----------
    nodes : int
        The total number of nodes in the graph
    height : float, optional
        The height in the inches of the drawn graph
    width : float, optional
        The width in the inches of the drawn graph
    """
    top_nodes = round(random.uniform(0.3*nodes, 0.7*nodes))
    bottom_nodes = nodes - top_nodes
    edges = round(nodes + random.uniform(0.1*nodes, 0.3*nodes))

    self._graph = DrawableGraph._connected_bipartite_graph(top_nodes, bottom_nodes, edges)
    self._nodes = [DrawableGraph.Node(value, self) for value in self._graph.nodes] 

    # set up drawing
    self._pos = nx.spring_layout(self._graph)
    plt.figure().set_figheight(height)
    if width:
      plt.figure().set_figwidth(width)

    self.draw()

  def _get_attributes(self, name):
    nx_attributes =  nx.get_node_attributes(self._graph, name)
    return {node.value:nx_attributes.get(node.value) for node in self.nodes}

  def _set_attributes(self, name, attributes):
    nx.set_node_attributes(self._graph, attributes, name=name)

  @property
  def nodes(self):
    """list of Nodes in the graph"""
    return self._nodes

  def get_node(self, value):
    """get a node from the graph

    Parameters
    ----------
    value : int
        value of the node to get 
       
    Returns
    -------
    Node
        the node with the given value if it exists, otherwise None
    """
    return self.nodes[value] if value in self._graph.nodes else None

  @property
  def colours(self):
    """dictionary mapping graph Nodes to their colours"""
    return self._get_attributes("colour") 

  @colours.setter
  def colours(self, value):
    self._set_attributes("colour", value)
    self.draw()

  def clear_colours(self):
    """clear the colours of all Nodes in graph"""
    self.colours = {node:None for node in self._graph.nodes}
    self.draw()

  def _draw(self):
    colours = [colour if colour else "white" for colour in self.colours.values()]
    nx.draw(self._graph, self._pos, with_labels=True, node_color=colours, edgecolors="black")

  def draw(self, pause=0.7):
    """draw the graph, or update the existing drawing if the graph has changed

    Parameters
    ----------
    pause : int, optional
        Time in seconds to wait before the next update (default is 1)
    """
    self._draw()
    plt.pause(pause)