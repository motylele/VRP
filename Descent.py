from Graph import Graph
from enum import Enum


class Neighborhood(Enum):
    INSERT = 1
    SWAP = 2

def display_solution(descent_instance):
    print(f"Solution =  {descent_instance[0]}")
    print(f"Total cost = {descent_instance[1]}")
    print("Index: [Route] | Vehicle capacity | Initial vehicle load")
    for idx, route in enumerate(descent_instance[2]):
        print(f"{idx}: {route} | {descent_instance[3][idx]} | {descent_instance[4][idx]} ")

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
    def calculate_cost(routes):
        total_cost = 0
        for route in routes:
            for vertex in range(len(route) - 1):
                u, v = route[vertex], route[vertex + 1]
                total_cost += graph.get_weight(u, v)
        return round(total_cost, 2)

    def check_if_can_serve(partial_solution, chosen_vehicle):
        demands = [graph.get_vertex(vertex).get_vertex_demand() for vertex in partial_solution]
        current_loads = [0] * len(demands)
        initial_load = 0

        for idx, demand in enumerate(demands):
            if demand > 0:
                if idx == 0:
                    current_loads[idx] = 0
                    initial_load = demand
                else:  # idx > 0
                    current_load = current_loads[idx - 1] - demand
                    if current_load > 0:
                        current_loads[idx] = current_load
                    else:  # current_load < 0
                        current_loads[idx] = 0

                    vertex_load = demand - current_loads[idx - 1]
                    if vertex_load > 0:
                        initial_load += vertex_load
            else:  # demand < 0
                demand = abs(demand)
                if idx == 0:
                    current_loads[idx] = demand
                    initial_load = 0
                else:  # idx > 0
                    current_loads[idx] = current_loads[idx - 1] + demand

        # Route simulating
        vehicle_load = initial_load
        for demand in demands:
            if vehicle_load > chosen_vehicle.capacity:
                return 0  # False
            vehicle_load -= demand
        return initial_load + 1  # True
                                 # initial_load = [0, vehicle_capacity]
                                 # initial_load + 1 = [1, vehicle_capacity + 1]

    def create_route(route, warehouse):
        return [warehouse.index] + list(route) + [warehouse.index]

    def fitness_function(solution):
        route = None
        route_load = None

        routes = []
        vehicles = []
        init_loads = []

        solution_idx = 0
        solution_begin = 0

        closest_warehouse = graph.get_closest_warehouse(solution[solution_idx])
        chosen_vehicle = closest_warehouse.select_vehicle()

        while solution_idx < len(solution):
            init_load = check_if_can_serve(solution[solution_begin:solution_idx+1], chosen_vehicle)

            if init_load:
                if route is None:
                    vehicles.append(chosen_vehicle.capacity)

                route = solution[solution_begin:solution_idx+1]
                route_load = init_load - 1
                solution_idx += 1
            else:
                solution_begin = solution_idx

                if route is not None:
                    routes.append(
                        create_route(
                            route,
                            closest_warehouse
                        )
                    )

                    closest_warehouse = graph.get_closest_warehouse(solution[solution_begin])
                    init_loads.append(route_load)
                    route = None
                chosen_vehicle = closest_warehouse.select_vehicle()

        if route:
            routes.append(
                create_route(
                    route,
                    closest_warehouse
                )
            )
            init_loads.append(route_load)

        return calculate_cost(routes), routes, vehicles, init_loads

    # Descent algorithm
    solution = graph.get_vertices_permutation()

    neighborhood = []
    if neighborhood_type == Neighborhood.INSERT:
        neighborhood = generate_insert_neighborhood(solution)

    if neighborhood_type == Neighborhood.SWAP:
        neighborhood = generate_swap_neighborhood(solution)

    solution_val, solution_routes, solution_vehicles, solution_init_loads = fitness_function(solution)
    solution_params = (
        solution,
        solution_val,
        solution_routes,
        solution_vehicles,
        solution_init_loads
    )

    for neighbor in neighborhood:
        neighbor_val, neighbor_routes, neighbor_vehicles, neighbor_init_loads = fitness_function(neighbor)

        if solution_params[1] > neighbor_val:
            solution_params = (
                neighbor,
                neighbor_val,
                neighbor_routes,
                neighbor_vehicles,
                neighbor_init_loads
            )

    return solution_params


vehicles_and_capacities = [
    (8, 6),  # 10 vehicles with capacity 12
    (5, 8)     # 5 vehicles with capacity 8
]

edges_range = (1.0, 10.0)
vertices_range = (0, 10)

graph = Graph(
    num_vertices=7,
    num_warehouses=3,
    vehicles_and_capacities=vehicles_and_capacities,
    generate_new_edges=False,
    edges_range=edges_range,
    generate_new_vertices=False,
    vertices_range=vertices_range
)

descent_instance = descent_algorithm(
    graph,
    neighborhood_type=Neighborhood.INSERT
)

display_solution(descent_instance)

graph.print_adj_matrix()
graph.print_client_vertices_params()
graph.print_graph_and_routes(descent_instance)