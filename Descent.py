from Graph import Graph


def generate_insert_neighborhood(S):
    neighborhood = []
    n = len(S)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = list(S)
                neighbor.insert(j, neighbor.pop(i))
                neighborhood.append(neighbor)
    return list(set(tuple(neighbor) for neighbor in neighborhood))


def generate_swap_neighborhood(S):
    neighborhood = []
    n = len(S)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = list(S)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighborhood.append(neighbor)
    return list(set(tuple(neighbor) for neighbor in neighborhood))

graph = Graph(
    num_vertices=7,
    num_warehouses=3,
    generate_new_data=False
)

S = graph.get_vertices_permutation() # len = 4
print(S)

insert_neighborhood = generate_insert_neighborhood(S)
print("\nINSERT NEIGHBORHOOD TYPE")
print(*insert_neighborhood, sep="\n")
print(len(insert_neighborhood))  # (n - 1)^2 -> (4-1)^2 = 9

swap_neighborhood = generate_swap_neighborhood(S)
print("\nSWAP NEIGHBORHOOD TYPE")
print(*swap_neighborhood, sep="\n")
print(len(swap_neighborhood))  # n(n - 1)/2 -> 4(4-1)/2 = 6
