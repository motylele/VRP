import numpy

from Descent import Neighborhood, display_solution
from Enums import Algorithm, Crossover
from Genetic import genetic_algorithm
from Graph import Graph
from HybridGenetic import hybrid_genetic_algorithm
from MultistartDescent import multistart_descent
from SimulatedAnnealing import simulated_annealing


vehicles_and_capacities = [
    (10, 12),  # 10 vehicles with capacity 12
    (5, 8)     # 5 vehicles with capacity 8
]

edges_range = (  # default values given
    1.0,  # min distance between two nodes
    10.0  # max
)
vertices_range = (  # default values given
    0,  # min value for both client vertex capacity and items stored
    10  # max
)

# Setting graph parameters
graph = Graph(
    num_vertices=7,
    num_warehouses=2,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=False,
    edges_range=edges_range,
    generate_new_vertices=False,
    vertices_range=vertices_range
)

# graph.print_client_vertices_params()
# graph.print_warehouse_vertices_params()
# graph.print_adj_matrix()
# graph.print_graph()


# Algorithm global params
# algorithm_type = Algorithm.MULTISTART_DESCENT
# algorithm_type = Algorithm.SIMULATED_ANNEALING
# algorithm_type = Algorithm.GENETIC_ALGORITHM
algorithm_type = Algorithm.HYBRID_GENETIC_ALGORITHM

time_limit = 1


if algorithm_type == Algorithm.MULTISTART_DESCENT:
    num_iterations = 9999

    # Run algorithm
    md_instance = multistart_descent(
        graph=graph,
        num_iterations=num_iterations,
        time_limit=time_limit,
        neighborhood_type=Neighborhood.INSERT  # or SWAP
    )

    # Displaying solution
    display_solution(md_instance)

    # Adjacency matrix
    graph.print_adj_matrix()

    # Displaying client vertices parameters
    graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    graph.print_graph_and_routes(md_instance)

elif algorithm_type == Algorithm.SIMULATED_ANNEALING:
    num_iterations = 100000
    initial_temperature = 30.0
    final_temperature = 0.7

    # Run algorithm
    sa_instance = simulated_annealing(
        graph=graph,
        num_iterations=num_iterations,
        time_limit=time_limit,
        initial_temperature=initial_temperature,
        final_temperature=final_temperature,
        neighborhood_type=Neighborhood.SWAP  # or SWAP
    )

    # Displaying solution
    display_solution(sa_instance)

    # Adjacency matrix
    graph.print_adj_matrix()

    # Displaying client vertices parameters
    graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    graph.print_graph_and_routes(sa_instance)

elif algorithm_type == Algorithm.GENETIC_ALGORITHM:
    num_generations = 9999  # todo: dodac w pracy
    # crossover_type = Crossover.SINGLE_POINT_CROSSOVER
    crossover_type = Crossover.ORDER_CROSSOVER

    ga_instance = genetic_algorithm(
        graph=graph,
        num_generations=num_generations,
        time_limit=time_limit,
        crossover_type=crossover_type,
    )

    # Displaying solution
    display_solution(ga_instance)

    # Adjacency matrix
    graph.print_adj_matrix()

    # Displaying client vertices parameters
    graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    graph.print_graph_and_routes(ga_instance)

elif algorithm_type == Algorithm.HYBRID_GENETIC_ALGORITHM:
    num_generations = 9999  # todo: add
    # crossover_type = Crossover.SINGLE_POINT_CROSSOVER
    crossover_type = Crossover.ORDER_CROSSOVER

    hg_instance = hybrid_genetic_algorithm(
        graph=graph,
        num_generations=num_generations,
        time_limit=time_limit,
        descent_percent=30,
        crossover_type=crossover_type
    )

    # Displaying solution
    display_solution(hg_instance)

    # Adjacency matrix
    # graph.print_adj_matrix()

    # Displaying client vertices parameters
    # graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    # graph.print_graph_and_routes(hg_instance)
else:
    print("No such option.")