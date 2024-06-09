import time
import random
import math


# Generating insert neighborhood
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


# Generating swap neighborhood
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


# Accepting result with given probability
def accept_with_probability(probability):
    return random.random() < probability


# Simulated annealing
def simulated_annealing(graph, num_iterations, time_limit, initial_temperature, final_temperature, neighborhood_type):

    # Calculating cost of given routes
    def calculate_cost(routes):
        total_cost = 0
        for route in routes:
            for vertex in range(len(route) - 1):
                u, v = route[vertex], route[vertex + 1]
                total_cost += graph.get_weight(u, v)
        return round(total_cost, 2)

    # Checking if vehicle with specified capacity can serve given solution
    def check_if_can_serve(partial_solution, chosen_vehicle):
        discharged = sum([graph.get_vertex(vertex).discharged for vertex in partial_solution])
        demands = [graph.get_vertex(vertex).get_vertex_demand() for vertex in partial_solution]
        current_loads = [0] * len(demands)
        initial_load = 0

        # Check number of batteries
        if discharged > chosen_vehicle.capacity:
            return None

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

        # Vehicle load check
        for current_load in current_loads:
            if current_load * 5 > chosen_vehicle.capacity - discharged:
                return None

        # Route simulating
        vehicle_load = initial_load * 5
        for demand in demands:
            if vehicle_load > chosen_vehicle.capacity - discharged:
                return None
            vehicle_load -= demand * 5

        return [initial_load, discharged]

    # Creating route, adding warehouses to both ends
    def create_route(route, warehouse):
        return [warehouse.index] + list(route) + [warehouse.index]

    # Fitness function calculating solution fitness value
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
            init_load = check_if_can_serve(solution[solution_begin:solution_idx + 1], chosen_vehicle)

            if init_load is not None:
                if route is None:
                    vehicles.append(chosen_vehicle.capacity)

                route = solution[solution_begin:solution_idx + 1]
                route_load = init_load
                solution_idx += 1
            else:  # init_load == 0
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

    # Simulated annealing algorithm
    beta = (initial_temperature - final_temperature) / ((num_iterations - 1) * initial_temperature * final_temperature)
    solution = graph.get_vertices_permutation()
    current_temperature = initial_temperature
    best_solution_params = (
        [],
        float('inf'),
        [],
        [],
        []
    )
    all_solutions = []

    start_time = time.time()
    for i in range(num_iterations):
        if time.time() - start_time >= time_limit:
            break

        neighborhood = []
        if neighborhood_type == neighborhood_type:
            neighborhood = generate_insert_neighborhood(solution)

        if neighborhood_type == neighborhood_type:
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
            probability = math.exp((solution_params[1] - neighbor_val) / current_temperature)

            if accept_with_probability(probability):
                solution_params = (
                    neighbor,
                    neighbor_val,
                    neighbor_routes,
                    neighbor_vehicles,
                    neighbor_init_loads
                )
                all_solutions.append(neighbor_val)

        if best_solution_params[1] > solution_params[1]:
            best_solution_params = solution_params

        if i < num_iterations - 1:
            current_temperature = current_temperature / (1 + beta * current_temperature)
    return best_solution_params, all_solutions
