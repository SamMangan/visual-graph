from visual_graph import VisualGraph

# Chosen from here: 
# https://davidmathlogic.com/colorblind/#%23648FFF-%23785EF0-%23DC267F-%23FE6100-%23FFB000
PINK = "#DC267F" 
YELLOW = "#FFB000"
ORANGE = "#FE6100"
BLUE = "#648FFF"

class Maze(VisualGraph):
  def __init__(self):
    super().__init__(type=VisualGraph.GraphType.GRID, grid_width=4, grid_height=3, update_interval=0)
    self.start = self.nodes[0]
    self.current = self.start
    self.current.colour = YELLOW
    self.points = 0
    self.energy = 5
    
    missing_links = [(0,4), (1,2), (9, 10)]
    for id1, id2 in missing_links:
      self.disconnect(self.get_node(id1), self.get_node(id2))
      
    self.items = [self.get_node(id) for id in [8, 10, 7]]
    self.finish = self.get_node(3) 
    for item in self.items:
      item.colour = ORANGE
    self.finish.colour = PINK

    edge_energies = {(0,1) : 1, (6,10) : 2}
    for (id1, id2), energy in edge_energies.items():
      edge = self.get_edge_between(self.get_node(id1), self.get_node(id2))
      edge.set_attribute("energy", energy)
    self.edge_label_attribute = "energy"
    
    self.draw(force_refresh=True)

  def goto(self, node):
    if node not in self.current.neighbours:
      print("You can't do that")
      return True

    edge = self.get_edge_between(self.current, node)
    energy = edge.get_attribute("energy", default=0)
    self.energy -= energy
    if self.energy > 0:
      print(f"Used {energy} points of energy. Remaining energy: {self.energy}")
    else:
      print(f"Game over! Score: {self.points}") 
      return False
    
    self.current.colour = None
    self.current = node
    self.current.colour = YELLOW

    if self.current == self.finish:
      print(f"Game over! Score: {self.points}") 
      return False

    if self.current in self.items:
      self.items.remove(self.current)
      self.points += 1
      print(f"Received 1 point. Total points: {self.points}")
    
    return True