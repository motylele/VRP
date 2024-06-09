import time

from APIKEY import api_key
import requests
import random

from Descent import display_solution
from Enums import Algorithm, Neighborhood, Crossover
from Genetic import genetic_algorithm
from Graph import Graph
from HybridGenetic import hybrid_genetic_algorithm
from MultistartDescent import multistart_descent
from SimulatedAnnealing import simulated_annealing


def get_matching_station_informations(prefix, limit):
    print("STATION_INFORMATIONS")

    response = requests.get(
        url="https://gbfs.urbansharing.com/rowermevo.pl/station_information.json",
        headers={'Client-Identifier': 'IDENTIFIER'})

    data = response.json()
    stations = data['data']['stations']

    count = 0
    for station in stations:
        if station['name'].startswith(prefix):
            yield station
            count += 1
            if count == limit:
                break


def get_matching_station_status(station_id):
    print("STATION STATUS")

    response = requests.get(
        url="https://gbfs.urbansharing.com/rowermevo.pl/station_status.json",
        headers={'Client-Identifier': 'IDENTIFIER'})

    data = response.json()
    stations = data['data']['stations']

    for station in stations:
        if station['station_id'] == station_id:
            return station

    return None


def extract_data(prefix, discharged_percent, limit=50):
    print("EXTRACT DATA")

    station_informations = get_matching_station_informations(prefix, limit)

    locations = [
        (54.43776163146023, 18.577104753732144),  # warehouse no 1
        (54.452542416881485, 18.554719346235462)]  # warehouse no 2

    num_warehouses = len(locations)

    with open("opendata/opendata_vertices", 'w') as file:
        for station in station_informations:

            capacity = station['capacity']
            station_status = get_matching_station_status(station['station_id'])
            stored = station_status['vehicle_types_available'][1]['count']

            if random.randint(1, 100) <= discharged_percent or stored == capacity:
                if stored != 0:
                    discharged = random.randint(1, stored)
            else:
                discharged = 0
            file.write(f"{discharged}, {capacity}, {stored}\n")
            locations.append((station['lat'], station['lon']))

    num_locations = len(locations)
    with open("opendata/opendata_edges", 'w') as file:
        for i in range(num_locations):
            for j in range(num_locations):
                if i != j:
                    file.write(f"{i - num_warehouses + 1}, "
                               f"{j - num_warehouses + 1}, "
                               f"{compute_distance(locations[i], locations[j])}\n")

    with open("opendata/opendata_locations", 'w') as file:
        for i in range(num_locations):
            print("ONE")
            file.write(f"{i - num_warehouses + 1}, {locations[i][0]}, {locations[i][1]}\n")
def compute_distance(loc1, loc2):
    print("COMPUTE DISTANCE")

    response = requests.get(
        url=f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={loc1[0]},{loc1[1]}"
            f"&destinations={loc2[0]},{loc2[1]}&key={api_key}"
    )

    data = response.json()

    if data["status"] == "OK":
        distance = data["rows"][0]["elements"][0]["distance"]["value"]
        return distance
    else:
        return None

# Generate new data
# extract_data("SOP", 30)


vehicles_and_capacities = [
    (8, 40),
    (10, 20),
]

# Setting graph parameters
graph = Graph(
    num_vertices=30,
    num_warehouses=2,
    vehicles_and_capacities=vehicles_and_capacities,
    filename_edges="opendata/opendata_edges",
    filename_vertices="opendata/opendata_vertices",
    real_data=True
)

graph.print_adj_matrix()
graph.print_client_vertices_params()

# algorithm_type = Algorithm.MULTISTART_DESCENT
# algorithm_type = Algorithm.SIMULATED_ANNEALING
# algorithm_type = Algorithm.GENETIC_ALGORITHM
algorithm_type = Algorithm.HYBRID_GENETIC_ALGORITHM
# algorithm_type = Algorithm.ALL

time_limit = 9999999
runs = 0

if algorithm_type == Algorithm.MULTISTART_DESCENT or algorithm_type == Algorithm.ALL:
    print("MD")

    num_iterations = 30
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
            file.write(f"{i + 1}: {md_instance}\n")

            # Displaying solution
            display_solution(md_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(md_instance)

if algorithm_type == Algorithm.SIMULATED_ANNEALING or algorithm_type == Algorithm.ALL:
    print("SA")

    num_iterations = 300
    initial_temperature = 120  # 50 # 120 # 220
    final_temperature = 10  # 1 # 10 # 15

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
            display_solution(sa_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(sa_instance)

if algorithm_type == Algorithm.GENETIC_ALGORITHM or algorithm_type == Algorithm.ALL:
    print("GA")

    num_generations = 30  # todo: dodac w pracy
    crossover_type = Crossover.ORDER_CROSSOVER
    # crossover_type = Crossover.SINGLE_POINT_CROSSOVER

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
            display_solution(ga_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(ga_instance)

if algorithm_type == Algorithm.HYBRID_GENETIC_ALGORITHM or algorithm_type == Algorithm.ALL:
    print("HG")

    num_generations = 70  # todo: dodac w pracy
    crossover_type = Crossover.ORDER_CROSSOVER
    # crossover_type = Crossover.SINGLE_POINT_CROSSOVER
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
            file.write(f"{i + 1}: {hg_instance}\n")

            # Displaying solution
            display_solution(hg_instance)

            # Adjacency matrix
            # graph.print_adj_matrix()

            # Displaying client vertices parameters
            # graph.print_client_vertices_params()

            # Displaying graph with overlaid solution routes
            # graph.print_graph_and_routes(hg_instance)