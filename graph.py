from visual_graph import VisualGraph

# Chosen from here: 
# https://davidmathlogic.com/colorblind/#%23648FFF-%23785EF0-%23DC267F-%23FE6100-%23FFB000
COLOUR_1 = "#DC267F" 
COLOUR_2 = "#FFB000"

class Graph(VisualGraph):
  def __init__(self, nodes=10):
    super().__init__(nodes=nodes)

  def _dfs(self, node, seen):
    node.colour = COLOUR_1
    for neighbour in node.neighbours:
        if not seen[neighbour]:
          seen[neighbour] = True
          self._dfs(neighbour, seen)
   
  def dfs(self, start_node):
    self.clear_colours()
    
    seen = {node:False for node in self.nodes}
    seen[start_node] = True
    
    self._dfs(start_node, seen)

  def bfs(self, start_node):
    self.clear_colours()
    
    seen = {node:False for node in self.nodes}
    seen[start_node] = True

    start_node.colour = COLOUR_1
    queue = [start_node]

    while queue:
      node = queue.pop(0)
      if node != start_node:
        if not node.colour:
          node.colour = COLOUR_1

      for neighbour in node.neighbours:
        if not seen[neighbour]:
          seen[neighbour] = True
          queue.append(neighbour)

  def two_colour(self, start_node):
    self.clear_colours()
    
    parent = {node:None for node in self.nodes}

    start_node.colour = COLOUR_1
    queue = [start_node]

    while queue:
      node = queue.pop(0)
      if node != start_node:
        if not node.colour:
          node.colour = COLOUR_2 if parent[node].colour == COLOUR_1 else COLOUR_1

      for neighbour in node.neighbours:
        if not parent[neighbour]:
          parent[neighbour] = node
          queue.append(neighbour)