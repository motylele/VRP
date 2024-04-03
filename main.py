from Graph import Graph

# Graph.generate_and_write_edges_to_file(7)
graph = Graph(3)
graph.read_edges_from_file()
graph.print_adj_matrix()
graph.print_graph()