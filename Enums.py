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
