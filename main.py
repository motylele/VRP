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
    num_vertices=100,
    num_warehouses=3,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=False,
    edges_range=edges_range,
    generate_new_vertices=False,
    vertices_range=vertices_range
)

# Algorithm global params
# algorithm_type = Algorithm.MULTISTART_DESCENT  # v:100, t:60 -> 489
# algorithm_type = Algorithm.SIMULATED_ANNEALING  # v:100, t:60 -> 548
# algorithm_type = Algorithm.GENETIC_ALGORITHM  # v:100, t:60 -> 524
# algorithm_type = Algorithm.HYBRID_GENETIC_ALGORITHM  # v:100, t:60 -> 510

time_limit = 60


if algorithm_type == Algorithm.MULTISTART_DESCENT:
    num_iterations = 50

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
    # graph.print_adj_matrix()

    # Displaying client vertices parameters
    # graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    # graph.print_graph_and_routes(md_instance)

elif algorithm_type == Algorithm.SIMULATED_ANNEALING:
    num_iterations = 30
    initial_temperature = 100.0
    final_temperature = 5.0

    # Run algorithm
    sa_instance = simulated_annealing(
        graph=graph,
        num_iterations=num_iterations,
        time_limit=time_limit,
        initial_temperature=initial_temperature,
        final_temperature=final_temperature,
        neighborhood_type=Neighborhood.INSERT  # or SWAP
    )

    # Displaying solution
    display_solution(sa_instance)

elif algorithm_type == Algorithm.GENETIC_ALGORITHM:
    num_generations = 30 # todo: add
    sol_per_pop = 10 #
    keep_parents = 1  # automat
    num_parents_mating = 2 # automat
    parent_selection_type = "sss"  #
    # crossover_type = Crossover.SINGLE_POINT_CROSSOVER
    crossover_type = Crossover.ORDER_CROSSOVER
    mutation_type = "swap"  #
    mutation_percent_genes = 20 #

    ga_instance = genetic_algorithm(
        graph=graph,
        num_generations=num_generations,
        time_limit=time_limit,
        sol_per_pop=sol_per_pop,
        keep_parents=keep_parents,
        num_parents_mating=num_parents_mating,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes
    )

    # Displaying solution
    # display_solution(ga_instance)

    # Adjacency matrix
    # graph.print_adj_matrix()

    # Displaying client vertices parameters
    # graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    # graph.print_graph_and_routes(ga_instance)

elif algorithm_type == Algorithm.HYBRID_GENETIC_ALGORITHM:
    num_generations = 20 # todo: add
    sol_per_pop = 10 #
    keep_parents = 1  # automat
    num_parents_mating = 2 # automat
    parent_selection_type = "sss"  #
    # crossover_type = Crossover.SINGLE_POINT_CROSSOVER
    crossover_type = Crossover.ORDER_CROSSOVER
    mutation_type = "swap"  #
    mutation_percent_genes = 20 #

    hg_instance = hybrid_genetic_algorithm(
        graph=graph,
        num_generations=num_generations,
        time_limit=time_limit,
        sol_per_pop=sol_per_pop,
        keep_parents=keep_parents,
        num_parents_mating=num_parents_mating,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes
    )

    # Displaying solution
    # display_solution(hg_instance)

    # Adjacency matrix
    # graph.print_adj_matrix()

    # Displaying client vertices parameters
    # graph.print_client_vertices_params()

    # Displaying graph with overlaid solution routes
    # graph.print_graph_and_routes(hg_instance)
else:
    print("No such option.")