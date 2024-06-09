from enum import Enum


# Choosing algorithm type
class Algorithm(Enum):
    MULTISTART_DESCENT = 1
    SIMULATED_ANNEALING = 2
    GENETIC_ALGORITHM = 3
    HYBRID_GENETIC_ALGORITHM = 4
    # ...
    ALL = 10


# [Neighborhood search] neighborhood selection type
class Neighborhood(Enum):
    INSERT = 1
    SWAP = 2


# [Evolutionary algorithms] crossover type
class Crossover(Enum):
    ORDER_CROSSOVER = 1
    SINGLE_POINT_CROSSOVER = 2


# Displaying algorithm output
def display_solution(algorithm_output):
    print(f"BEST SOLUTION =  {algorithm_output[0]}")
    print(f"TOTAL COST = {algorithm_output[1]}")
    print("ROUTES (Index: Vehicle capacity | Initial bikes load | Initial batteries load | [Route]):")
    for idx, route in enumerate(algorithm_output[2]):
        print(f"{idx:3}: {algorithm_output[3][idx]:5} | {algorithm_output[4][idx][0]:5}| {algorithm_output[4][idx][1]:5} | {route}")
