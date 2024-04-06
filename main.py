from Graph import Graph


graph = Graph(
    num_vertices=4,
    num_warehouses=3,
    generate_new_data=True,
)

graph.print_adj_matrix()
graph.print_graph()
