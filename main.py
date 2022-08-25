from graph import Graph
from maze import Maze
import os

def try_again(error_msg=None):
  if error_msg:
    print(error_msg)
  input("Press any key to continue...")

def graph_traversals():
  g = Graph(10)

  while True:
    os.system("clear")
    action = input("Choose an action: [r]egenerate, [b]fs, [d]fs, [t]wo_colour\n")
    
    if action == "r":
      g = Graph(10)
      
    elif action in "bdt":
      value = input("Choose start node:\n")
      
      if not value.isnumeric():
        try_again(f"{value} is not a number")
        continue
      start_node = g.get_node(int(value))
      if not start_node: 
        try_again(f"{value} is not in the graph")
        continue
      
      if action == "b":
        g.bfs(start_node)
      elif action == "d":
        g.dfs(start_node)
      elif action == "t":
        g.two_colour(start_node)
        
    else:
      try_again(f"{action} is not a valid action")

def maze_game():
  m = Maze(10)

  while True:
    cmd = input("> ")
    name, *args = cmd.split()

    if name == "regenerate":
      m = Maze(10)
      
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
      
  
#graph_traversals()
maze_game()