import os
from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx

from utils import grid_layout, create_bipartite_graph, create_grid_graph
 
class VisualGraph:
  """
  A graph with nodes and edges which can be drawn.
  """

  class GraphType(Enum):
    BIPARTITE = 0
    GRID = 1
  
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
      
    def __eq__(self, other):
      return self.value == other.value

    def __gt__(self, other):
      return self.value > other.value

    def _get_attribute(self, name):
      return self._graph._graph.nodes[self.value].get(name)

    def _set_attribute(self, name, value):
      self._graph._graph.nodes[self.value][name] = value

    @property
    def colour(self):
      """string representing the colour of this Node"""
      return self._get_attribute("colour")

    @colour.setter
    def colour(self, colour):
      self._set_attribute("colour", colour)
      self._graph.draw()

    def connect(self, node):
      self._graph.connect(self, node)

    @property
    def grid_neighbours(self):
      nx_neighbours = self._graph._graph.neighbors(self.value)
      return [self._graph._nodes[neighbour] for neighbour in nx_neighbours]

    @property
    def neighbours(self):
      """list of Nodes neigbouring this Node in the graph"""
      nx_neighbours = self._graph._graph.neighbors(self.value)
      return [self._graph._nodes[neighbour] for neighbour in nx_neighbours]

  class Edge:
    def __init__(self, node1, node2, graph):
      self.node1 = node1
      self.node2 = node2
      self._graph = graph
      self.value  = 3

    def __repr__(self):
      return f"Edge({self.node1}, {self.node2})"

    def set_attribute(self, name, value):
      self._graph._graph[self.node1][self.node2][name] = value
      
    def get_attribute(self, name, default=None):
      return self._graph._graph.get_edge_data(self.node1, self.node2, {}).get(name, default) 

  
  def __init__(self, type=GraphType.BIPARTITE, nodes=10, grid_width=4, grid_height=4, update_interval=1, width=6, height=4):
    """
    Parameters
    ----------
    type : VisualGraph.GraphType, optional (default=VisualGraph.GraphType.BIPARTITE)
        The type of graph. Options are:
          BIPARTITE: A randomly generated bipartite (two-colourable) graph
          GRID: A graph whose nodes are connected in a 2D grid/lattice pattern
    nodes : int, optional (default=10)
        The total number of nodes in BIPARTITE graph 
    grid_width : int, optional (default=4)
        The number of nodes wide for the GRID graph
    grid_height : int, optional (default=4)
        The number of nodes high for the GRID graph
    update_interval : float, optional (default=1)
        The time in seconds between drawing updates (set to 0 for instant updates)
    width : float, optional (default=4)
        The width in inches of the drawn graph
    height : float, optional (default=4)
        The height in inches of the drawn graph
    """
    self.update_interval = update_interval
    self._graph = None
    self._pos = None
    self._layout_function = None
    self._nodes = {}
    self._edges = {}
    self.height = height
    self.width = width
    self.grid_height = grid_height
    self.grid_width = grid_width
    self.edge_label_attribute = None

    #TODO validate figure and graph height and width values ...
    
    if type == VisualGraph.GraphType.BIPARTITE:
      #TODO log a warning if GRID details were supplied
      if not nodes:
        self._graph = nx.Graph()
        return
      self._graph = create_bipartite_graph(nodes)
      self._layout_function = lambda : nx.spring_layout(self._graph)
    elif type == VisualGraph.GraphType.GRID:
      #TODO log a warning if BIPARTITE details were supplied
      self._graph = create_grid_graph(self.grid_width, self.grid_height)
      self._layout_function = lambda : grid_layout(self.width, self.height, self.grid_width, self.grid_height)
    else:
      assert False, f"{type} is not a supported GraphType"

    self._pos = self._layout_function() 
    self._nodes = {value: VisualGraph.Node(value, self) for value in self._graph.nodes}
    self._edges = {(node1, node2): VisualGraph.Edge(node1, node2, self) for node1, node2 in self._graph.edges}

    # set up drawing 
    plt.figure().set_size_inches(self.width, self.height)
    self.draw()

  def create_node(self, value):      #self._graph.colours = {self.value:colour}

    node = VisualGraph.Node(value, self)
    self._graph.add_node(value)
    self._nodes[value] = node #TODO make this a property
    return node

  def connect(self, node1, node2):
    self._graph.add_edge(node1.value, node2.value)
    self._edges[(node1.value, node2.value)] =  VisualGraph.Edge(node1.value, node2.value, self)

  def disconnect(self, node1, node2):
    self._graph.remove_edge(node1.value, node2.value)
    self._edges.pop((node1.value, node2.value))

  def _get_attributes(self, name):
    nx_attributes =  nx.get_node_attributes(self._graph, name)
    return {node:nx_attributes.get(node) for node in self._nodes}

  def _set_attributes(self, name, attributes):
    nx.set_node_attributes(self._graph, attributes, name=name)

  @property
  def nodes(self):
    """list of Nodes in the graph"""
    return list(self._nodes.values())

  @property
  def edges(self):
    """list of edges in the graph"""
    return list(self._edges.values())

  def get_edge_between(self, node1, node2):
    if node1 > node2:
      node1, node2 = node2, node1 # reorder
    return self._edges[(node1.value, node2.value)]
  
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
    self.colours = {node:None for node in self._nodes}
    self.draw()

  def _draw(self):
    colours = [colour if colour else "white" for colour in self.colours.values()]
    nx.draw(self._graph, self._pos, with_labels=True, node_color=colours, edgecolors="black")
    edge_labels = {nodes:edge.get_attribute(self.edge_label_attribute, 0) for nodes, edge in self._edges.items()}
    nx.draw_networkx_edge_labels(self._graph, edge_labels=edge_labels, pos=self._layout_function())

  def draw(self, force_refresh=False, force_layout_refresh=False):
    """draw the graph, or update the existing drawing if the graph has changed
    """
    if force_refresh:
      plt.clf()
    if force_layout_refresh:
      self._pos = self._layout_function()
    
    self._draw()

    if self.update_interval > 0:
      plt.pause(self.update_interval)
    else:
      plt.show(block=False)