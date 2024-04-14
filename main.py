from enum import Enum
from Descent import descent_algorithm, Neighborhood, display_solution
from Graph import Graph
from MultistartDescent import multistart_descent


# Enum for choosing algorithm
class Algorithm(Enum):
    MULTISTART_DESCENT = 1
    SIMULATED_ANNEALING = 2
    GENETIC_ALGORITHM = 3
    HYBRID_GENETIC_ALGORITHM = 4


vehicles_and_capacities = [
    (10, 12),  # 10 vehicles with capacity 12
    (5, 8)     # 5 vehicles with capacity 8
]

edges_range = (
    1.0,  # min distance between two nodes
    10.0  # max
)
vertices_range = (
    0,  # min value for both client vertex capacity and items stored
    10  # max
)

# Setting graph parameters
graph = Graph(
    num_vertices=8,
    num_warehouses=3,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=True,
    edges_range=edges_range,
    generate_new_vertices=True,
    vertices_range=vertices_range
)

# Choosing algorithm type
algorithm_type = Algorithm.MULTISTART_DESCENT


if algorithm_type == Algorithm.MULTISTART_DESCENT:
    num_iterations = 5
    time_limit = 30

    # Run algorithm
    multistart_instance = multistart_descent(
        graph,
        num_iterations,
        time_limit,
        Neighborhood.INSERT  # or SWAP
    )

    # Displaying solution
    display_solution(multistart_instance)

    # Adjacency matrix
    graph.print_adj_matrix()

    # Displaying client vertices parameters
    graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    graph.print_graph_and_routes(multistart_instance)

elif algorithm_type == Algorithm.MULTISTART_DESCENT:
    print("WIP")
elif algorithm_type == Algorithm.MULTISTART_DESCENT:
    print("WIP")
elif algorithm_type == Algorithm.MULTISTART_DESCENT:
    print("WIP")
else:
    print("No such option.")

