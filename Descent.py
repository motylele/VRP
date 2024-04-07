from Graph import Graph
from enum import Enum
import random


class Neighborhood(Enum):
    INSERT = 1
    SWAP = 2


def descent_algorithm(graph, neighborhood_type=Neighborhood.INSERT, print_neighborhood=False):
    solution = graph.get_vertices_permutation()

    neighborhood = []
    if neighborhood_type == Neighborhood.INSERT:
        neighborhood = generate_insert_neighborhood(solution, print_neighborhood)

    if neighborhood_type == Neighborhood.SWAP:
        neighborhood = generate_swap_neighborhood(solution, print_neighborhood)

    for candidate_solution in neighborhood:
        if fitness_function(solution) > fitness_function(candidate_solution):
            solution = candidate_solution

    return solution


def fitness_function(solution):  # todo: implementation
    return solution[0] * 1 + solution[1] * 10 + solution[2] * 100 + solution[3] * 1000


def generate_insert_neighborhood(solution, print_neighborhood):  # size: (n - 1)^2
    neighborhood = []
    n = len(solution)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = list(solution)
                neighbor.insert(j, neighbor.pop(i))
                neighborhood.append(neighbor)
    neighborhood = list(set(tuple(neighbor) for neighbor in neighborhood))
    if print_neighborhood:
        print(f"\nNEIGHBORHOOD TYPE: INSERT, size = {len(neighborhood)}")
        print(*neighborhood, sep="\n")
    return neighborhood


def generate_swap_neighborhood(solution, print_neighborhood):  # size: n(n - 1)/2
    neighborhood = []
    n = len(solution)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = list(solution)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighborhood.append(neighbor)
    neighborhood = list(set(tuple(neighbor) for neighbor in neighborhood))
    if print_neighborhood:
        print(f"\nNEIGHBORHOOD TYPE: SWAP, size = {len(neighborhood)}")
        print(*neighborhood, sep="\n")
    return neighborhood


graph = Graph(
    num_vertices=7,
    num_warehouses=3,
    generate_new_edges=False,
    generate_new_vertices=False
)

print(descent_algorithm(
    graph,
    neighborhood_type=Neighborhood.INSERT,
    print_neighborhood=False
))

for i in graph.list_vertex:
    print(i.capacity, i.stored)
