import time

from Descent import Neighborhood, display_solution
from Enums import Algorithm, Crossover
from Genetic import genetic_algorithm
from Graph import Graph
from HybridGenetic import hybrid_genetic_algorithm
from MultistartDescent import multistart_descent
from SimulatedAnnealing import simulated_annealing

vehicles_and_capacities = [
    (8, 15),   # 8 vehicles with capacity 12
    (3, 10),   # 3 vehicles with capacity 10
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
    num_vertices=10,
    num_warehouses=2,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=False,
    filename_edges="data/graph-edges.txt",
    edges_range=edges_range,
    generate_new_vertices=False,
    filename_vertices="data/graph-vertices.txt",
    vertices_range=vertices_range
)

# Display clients params
graph.print_client_vertices_params()

# Display warehouses params
# graph.print_warehouse_vertices_params()

# Display adjacency matrix
# graph.print_adj_matrix()

# Display graph
# graph.print_graph()


# Algorithm global params
algorithm_type = 0

algorithm_type = Algorithm.MULTISTART_DESCENT
# algorithm_type = Algorithm.SIMULATED_ANNEALING
# algorithm_type = Algorithm.GENETIC_ALGORITHM
# algorithm_type = Algorithm.HYBRID_GENETIC_ALGORITHM
# algorithm_type = Algorithm.ALL

time_limit = 6666
runs = 1

if algorithm_type == Algorithm.MULTISTART_DESCENT or algorithm_type == Algorithm.ALL:

    num_iterations = 10
    neighborhood_type = Neighborhood.INSERT
    # neighborhood_type = Neighborhood.SWAP

    with open("output/md.txt", 'w') as file:
        for i in range(runs):
            print(f"Iteration {i + 1} of {runs}")

            start_time = time.time()

            # Run algorithm
            md_instance, all_solutions = multistart_descent(
                graph=graph,
                num_iterations=num_iterations,
                time_limit=time_limit,
                neighborhood_type=neighborhood_type
            )

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Czas działania algorytmu: {elapsed_time} sekund")

            # Write to file
            file.write(f"{i + 1}:\n {md_instance}\n {all_solutions}\n\n")

            # Displaying solution
            display_solution(md_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(md_instance)

if algorithm_type == Algorithm.SIMULATED_ANNEALING or algorithm_type == Algorithm.ALL:

    num_iterations = 80  # 3300 #
    initial_temperature = 220  # 50 # 120 # 220
    final_temperature = 15  # 1 # 10 # 15

    # neighborhood_type = Neighborhood.INSERT
    neighborhood_type = Neighborhood.SWAP

    with open("output/sa.txt", 'w') as file:
        for i in range(runs):
            print(f"Iteration {i + 1} of {runs}")

            start_time = time.time()

            # Run algorithm
            sa_instance, all_solutions = simulated_annealing(
                graph=graph,
                num_iterations=num_iterations,
                time_limit=time_limit,
                initial_temperature=initial_temperature,
                final_temperature=final_temperature,
                neighborhood_type=neighborhood_type
            )

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Czas działania algorytmu: {elapsed_time} sekund")

            # Write to file
            file.write(f"{sa_instance[1]}\n")

            # Displaying solution
            # display_solution(sa_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(sa_instance)

if algorithm_type == Algorithm.GENETIC_ALGORITHM or algorithm_type == Algorithm.ALL:

    num_generations = 50  # todo: dodac w pracy
    # crossover_type = Crossover.ORDER_CROSSOVER
    crossover_type = Crossover.SINGLE_POINT_CROSSOVER

    with open("output/ga.txt", 'w') as file:
        for i in range(runs):
            print(f"Iteration {i + 1} of {runs}")

            start_time = time.time()

            ga_instance, all_solutions = genetic_algorithm(
                graph=graph,
                num_generations=num_generations,
                time_limit=time_limit,
                crossover_type=crossover_type,
            )

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Czas działania algorytmu: {elapsed_time} sekund")

            # Write to file
            file.write(f"{i + 1}:\n {ga_instance}\n {all_solutions}\n\n")

            # Displaying solution
            # display_solution(ga_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(ga_instance)

if algorithm_type == Algorithm.HYBRID_GENETIC_ALGORITHM or algorithm_type == Algorithm.ALL:

    num_generations = 10  # todo: dodac w pracy
    # crossover_type = Crossover.ORDER_CROSSOVER
    crossover_type = Crossover.SINGLE_POINT_CROSSOVER
    # neighborhood_type = Neighborhood.INSERT
    neighborhood_type = Neighborhood.SWAP

    with open("output/hg.txt", 'w') as file:
        for i in range(runs):
            print(f"Iteration {i + 1} of {runs}")

            start_time = time.time()

            hg_instance, all_solutions = hybrid_genetic_algorithm(
                graph=graph,
                num_generations=num_generations,
                time_limit=time_limit,
                descent_percent=30,
                crossover_type=crossover_type,
                neighborhood_type=neighborhood_type
            )

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Czas działania algorytmu: {elapsed_time} sekund")

            # Write to file
            file.write(f"{i + 1}:\n {hg_instance}\n {all_solutions}\n\n")

            # Displaying solution
            # display_solution(hg_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(hg_instance)