from graph import Graph
import os

g = Graph(10)

def try_again(error_msg):
  print(error_msg)
  input("Press any key to try again...")

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