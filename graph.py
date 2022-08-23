from drawable_graph import DrawableGraph

# Chosen from here: 
# https://davidmathlogic.com/colorblind/#%23648FFF-%23785EF0-%23DC267F-%23FE6100-%23FFB000
COLOUR_1 = "#DC267F" 
COLOUR_2 = "#FFB000"

class Graph(DrawableGraph):
  def __init__(self, nodes, edges):
    super().__init__(nodes, edges)
    print(self.__dir__())

  def bfs(self, start_node):
    seen = {node:False for node in self.nodes}

    start_node.colour = COLOUR_1
    queue = [start_node]
    seen[start_node] = True

    while queue != []:
      node = queue.pop(0)
      if node != start_node:
        if node.colour == "grey":
          node.colour = COLOUR_1
          self.update_drawing()

      print(node)
      for neighbour in node.neighbours:
        if not seen[neighbour]:
          seen[neighbour] = node
          queue.append(neighbour)

  def two_colour(self, start_node):
    parent = {node:None for node in self.nodes}

    start_node.colour = COLOUR_1
    queue = [start_node]

    while queue != []:
      node = queue.pop(0)
      if node != start_node:
        if not node.colour:
          print(f"{node} {parent[node]} {parent[node].colour}")
          node.colour = COLOUR_2 if parent[node].colour == COLOUR_1 else COLOUR_1
          self.update_drawing()

      print(node)
      for neighbour in node.neighbours:
        if not parent[neighbour]:
          parent[neighbour] = node
          queue.append(neighbour)