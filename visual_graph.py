from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx
import random

class VisualGraph:

  class GraphType(Enum):
    BIPARTITE = 0
    GRID = 1

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

    def connect(self, node):
      self._graph.connect(self, node)

    @property
    def neighbours(self):
      """list of Nodes neigbouring this Node in the graph"""
      nx_neighbours = self._graph._graph.neighbors(self.value)
      return [self._graph._nodes[neighbour] for neighbour in nx_neighbours]

  def _init_bipartite_graph(self, nodes):
    top_nodes = round(random.uniform(0.3*nodes, 0.7*nodes))
    bottom_nodes = nodes - top_nodes
    edges = round(nodes + random.uniform(0.1*nodes, 0.3*nodes))

    self._graph = None
    #print(f"Creating a bipartite graph with {n} nodes in one set, {m} nodes in the other set, and {k} edges")
    while True:
      self._graph = nx.bipartite.gnmk_random_graph(top_nodes, bottom_nodes, edges)
      if nx.is_connected(self._graph):
        break
      #print("Graph was not connected, trying again")
    #print("Done")

    self._layout_function = lambda f: nx_spring_layout(self._graph)
    
  def _init_grid_graph(self):
      self._graph = nx.Graph() 
      id = 0
      for row in range(self.grid_height):
        for col in range(self.grid_width):
          self.create_node(id)
          id += 1

      # connect nodes in each row
      for col in range(1, self.grid_width):
        for row in range(self.grid_height):
          node = self.grid_width*row + col
          self.connect(self.get_node(node - 1), self.get_node(node))

      # connect nodes in each column
      for row in range(1, self.grid_height):
        for col in range(self.grid_width):
          node = self.grid_width*row + col
          self.connect(self.get_node(node - self.grid_width), self.get_node(node))

      # compute the node positions
      def grid_layout():
        x_spacing = self.width / (self.grid_width - 1)
        y_spacing = self.height / (self.grid_height - 1)
        pos = {}
        for row in range(self.grid_height):
          for col in range(self.grid_width):
            node = self.grid_width*row + col
            x = col * x_spacing
            y = row * y_spacing
            pos[node] = (x, y)
        return pos
      self._layout_function = grid_layout
  
  def __init__(self, type=GraphType.BIPARTITE, nodes=10, grid_height=4, grid_width=4, update_interval=1, height=4, width=6):
    """
    Parameters
    ----------
    type : VisualGraph.GraphType, optional (default=VisualGraph.GraphType.BIPARTITE)
        The type of graph. Options are:
          BIPARTITE: A randomly generated bipartite (two-colourable) graph
          GRID: A graph whose nodes are connected in a 2D grid/lattice pattern
    nodes : int, optional (default=10)
        The total number of nodes in BIPARTITE graph 
    grid_height : int, optional (default=4)
        The number of nodes high for the GRID graph
    grid_width : int, optional (default=4)
        The number of nodes wide for the GRID graph
    update_interval : float, optional (default=1)
        The time in seconds between drawing updates (set to 0 for instant updates)
    height : float, optional (default=4)
        The height in inches of the drawn graph
    width : float, optional (default=4)
        The width in inches of the drawn graph
    """
    self.update_interval = update_interval
    self._graph = None
    self._pos = None
    self._layout_function = None
    self._nodes = {}
    self.height = height
    self.width = width
    self.grid_height = grid_height
    self.grid_width = grid_width
    
    if type == VisualGraph.GraphType.BIPARTITE:
      #TODO log a warning if GRID details were supplied
      if not nodes:
        self._graph = nx.Graph()
        return
      self._init_bipartite_graph(nodes)
    elif type == VisualGraph.GraphType.GRID:
      #TODO log a warning if BIPARTITE details were supplied
      #TODO raise exception if height and width < 1
      self._init_grid_graph()
    else:
      assert False, f"{type} is not a supported GraphType"

    self._pos = self._layout_function() 
    self._nodes = {value: VisualGraph.Node(value, self) for value in self._graph.nodes}

    # set up drawing 
    plt.figure().set_size_inches(self.width, self.height)
    self.draw()

  def create_node(self, value):
    node = VisualGraph.Node(value, self)
    self._graph.add_node(value)
    self._nodes[value] = node #TODO make this a property
    #self._pos = self._layout_function(self._graph)
    return node

  def connect(self, node1, node2):
    self._graph.add_edge(node1.value, node2.value)
    #self._pos = self._layout_function(self._graph)

  def disconnect(self, node1, node2):
    self._graph.remove_edge(node1.value, node2.value)

  def _get_attributes(self, name):
    nx_attributes =  nx.get_node_attributes(self._graph, name)
    return {node:nx_attributes.get(node) for node in self._nodes}

  def _set_attributes(self, name, attributes):
    nx.set_node_attributes(self._graph, attributes, name=name)

  @property
  def nodes(self):
    """list of Nodes in the graph"""
    return list(self._nodes.values())

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

  def draw(self, force_refresh=False):
    """draw the graph, or update the existing drawing if the graph has changed
    """
    if force_refresh:
      plt.clf()
    
    self._draw()

    if self.update_interval > 0:
      plt.pause(self.update_interval)
    else:
      plt.show(block=False)