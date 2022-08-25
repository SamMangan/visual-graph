from drawable_graph import DrawableGraph
import random

# Chosen from here: 
# https://davidmathlogic.com/colorblind/#%23648FFF-%23785EF0-%23DC267F-%23FE6100-%23FFB000
PINK = "#DC267F" 
YELLOW = "#FFB000"
ORANGE = "#FE6100"
BLUE = "#648FFF"

class Maze(DrawableGraph):
  def __init__(self, nodes):
    super().__init__(nodes, update_interval=0)
    self.start = self.nodes[0]
    self.current = self.start
    self.current.colour = YELLOW
    self.points = 0

    choices = list(set(self.nodes) - set(self.current.neighbours) - {self.current})
    self.item, self.finish = random.choices(choices, k=2) 
    self.item.colour = ORANGE
    self.finish.colour = PINK

  def goto(self, node):
    if node not in self.current.neighbours:
      print("You can't do that")
      return True
      
    self.current.colour = None
    self.current = node
    self.current.colour = YELLOW

    if self.current == self.finish:
      print(f"Game over! Score={self.points}") 
      return False

    if self.current == self.item:
      self.points += 1
      print(f"Received 1 point. Total points: {self.points}")
    
    return True