from graph import Graph

g = Graph(10)
#g.draw()
start_node = g.nodes[0]
g.two_colour(start_node)
#g.bfs(start_node)