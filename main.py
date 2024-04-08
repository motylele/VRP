from Graph import Graph

vehicles_and_capacities = [
    (10, 12),  # 10 vehicles with capacity 12
    (5, 8)     # 5 vehicles with capacity 8
]

graph = Graph(
    num_vertices=7,
    num_warehouses=3,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=True,
    generate_new_vertices=True
)