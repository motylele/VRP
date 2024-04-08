import random

from Vehicle import Vehicle
from Graph import Graph
from enum import Enum


class Neighborhood(Enum):
    INSERT = 1
    SWAP = 2

# todo: fitness_function implementation
'''
steps:
    - get random vehicle with a probability advantage for cars with larger capacity
    - divide permutation into routes, if needed get another car
    - repeat until all permutation covered
    - compute and return costs
    
example fitness_function for getting decreasing sequence (len = 4):
    - return solution[0] * 1 + solution[1] * 10 + solution[2] * 100 + solution[3] * 1000  # best sol:. a1 > .. > a4
'''


def generate_insert_neighborhood(solution):  # size: (n - 1)^2
    neighborhood = []
    n = len(solution)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = list(solution)
                neighbor.insert(j, neighbor.pop(i))
                neighborhood.append(neighbor)
    return list(set(tuple(neighbor) for neighbor in neighborhood))


def generate_swap_neighborhood(solution):  # size: n(n - 1)/2
    neighborhood = []
    n = len(solution)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = list(solution)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighborhood.append(neighbor)
    return list(set(tuple(neighbor) for neighbor in neighborhood))


def descent_algorithm(graph, neighborhood_type=Neighborhood.INSERT):

    def fitness_function(solution):
        closest_warehouse = graph.get_closest_warehouse(solution[0])
        chosen_vehicle = closest_warehouse.select_vehicle()

        return random.randint(0, 10)  # temp solution

    solution = graph.get_vertices_permutation()

    neighborhood = []
    if neighborhood_type == Neighborhood.INSERT:
        neighborhood = generate_insert_neighborhood(solution)

    if neighborhood_type == Neighborhood.SWAP:
        neighborhood = generate_swap_neighborhood(solution)

    for candidate_solution in neighborhood:
        if fitness_function(solution) > fitness_function(candidate_solution):
            solution = candidate_solution

    return solution


vehicles_and_capacities = [
    (10, 12),  # 10 vehicles with capacity 12
    (5, 8)     # 5 vehicles with capacity 8
]

graph = Graph(
    num_vertices=7,
    num_warehouses=3,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=False,
    generate_new_vertices=False
)

descent_algorithm(
    graph,
    neighborhood_type=Neighborhood.INSERT
)

graph.print_graph()