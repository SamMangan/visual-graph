from visual_graph import VisualGraph, VisualNode

# Chosen from here: 
# https://davidmathlogic.com/colorblind/#%23648FFF-%23785EF0-%23DC267F-%23FE6100-%23FFB000
PINK = "#DC267F" 
YELLOW = "#FFB000"
ORANGE = "#FE6100"
BLUE = "#648FFF"

class Maze(VisualGraph):
  def __init__(self, ascii_mode=False, auto_redraw=True):
    super().__init__(type=VisualGraph.GraphType.GRID, grid_width=4, grid_height=3, update_interval=0, ascii_mode=ascii_mode, auto_redraw=auto_redraw)
    self.start = self.nodes[0]
    self.current = self.start
    self.current.colour = YELLOW
    self.points = 0
    self.energy = 5
    
    missing_links = [(0,4), (1,2), (9, 10)]
    for id1, id2 in missing_links:
      self.disconnect(VisualNode(id1), VisualNode(id2))
      
    self.items = [VisualNode(id) for id in [8, 10, 7]]
    self.finish = VisualNode(3) 
    for item in self.items:
      item.colour = ORANGE
    self.finish.colour = PINK

    edge_energies = {(0,1) : 1, (6,10) : 2}
    for (id1, id2), energy in edge_energies.items():
      edge = self.get_edge_between(VisualNode(id1), VisualNode(id2))
      edge.value = energy
    
    self.draw(force_refresh=True)

  def goto(self, node):
    if node not in self.current.neighbours:
      print("You can't do that")
      return True

    edge = self.get_edge_between(self.current, node)
    
    self.current.colour = None
    self.current = node
    self.current.colour = YELLOW

    if not self.auto_redraw:
      self.draw()

    energy = edge.value
    self.energy -= energy
    if self.energy > 0:
      print(f"Used {energy} points of energy. Remaining energy: {self.energy}")
    else:
      print(f"Game over! Score: {self.points}") 
      return False

    if self.current == self.finish:
      print(f"Game over! Score: {self.points}") 
      return False

    if self.current in self.items:
      self.items.remove(self.current)
      self.points += 1
      print(f"Received 1 point. Total points: {self.points}")
    
    return True


def maze_game():
  ascii_mode = False
  m = Maze(ascii_mode=ascii_mode, auto_redraw=(not ascii_mode))

  while True:
    cmd = input("> ")
    name, *args = cmd.split()

    if name == "regenerate":
      m = Maze()
      
    elif name == "goto":

      if len(args) < 1:
        print("1 argument expected")
        continue
      value = args[0]
      if not value.isnumeric():
        print(f"{value} is not a number")
        continue
      node = m.get_node(int(value))
      if not node: 
        print(f"{value} is not in the graph")
        continue

      if not m.goto(node):
        break
