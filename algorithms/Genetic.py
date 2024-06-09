from architecture.Utils import Crossover
import warnings
import pygad
import numpy
import time

# Ignore constant warning
warnings.filterwarnings("ignore", message="The 'delay_after_gen' parameter is deprecated*")


def genetic_algorithm(
        graph,
        num_generations,
        time_limit,
        crossover_type):

    # 'Global' time counter
    time_start = 0

    # Global list to store best solution
    solution_params = (
        [],             # solution
        float('-inf'),  # solution_val
        [],             # solution_routes
        [],             # solution_vehicles
        []              # solution_init_loads
    )

    all_solutions = []

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

    # Roulette selection method
    def roulette_selection(fitness, num_parents, ga_instance):
        total_fitness = numpy.sum(fitness)

        probabilities = fitness / total_fitness

        selected_indices = numpy.random.choice(range(len(fitness)), size=num_parents, p=probabilities)
        selected_parents = ga_instance.population[selected_indices]

        return selected_parents, selected_indices

    # modified 1PX crossover
    def one_point_crossover(parents, offspring_size, ga_instance):
        offspring = []
        idx = 0
        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

            split_point = numpy.random.choice(range(offspring_size[1]))

            parent1[split_point:] = parent2[split_point:]

            offspring.append(parent1)

            idx += 1

        return numpy.array(offspring)

    # OX crossover
    def order_crossover(parents, offspring_size, ga_instance):
        offspring = []
        idx = 0
        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

            split_points = sorted(numpy.random.choice(range(offspring_size[1]), size=2))

            mask = numpy.zeros(offspring_size[1], dtype=bool)
            mask[split_points[0]:split_points[1] + 1] = True

            offspring_candidate = parent1[split_points[0]:split_points[1] + 1]

            idx_parent2 = 0
            for i in range(offspring_size[1]):
                if not mask[i]:
                    while parent2[idx_parent2] in offspring_candidate:
                        idx_parent2 += 1
                    offspring_candidate = numpy.insert(offspring_candidate, i, parent2[idx_parent2])
                    idx_parent2 += 1
            offspring.append(offspring_candidate)

            idx += 1

        return numpy.array(offspring)

    # Stop algorithm on given time
    def stop_at_generation(ga_instance):
        if time.time() - time_start >= time_limit:
            return "stop"

    # Setting proper population size, depending on chromosome len
    def calculate_population_size(chromosome_length):
        coefficient = 3
        offset = 10
        population_size = int(coefficient * chromosome_length + offset)
        return population_size

    # Fitness function calculating solution fitness value
    def fitness_function(ga_instance, solution, solution_id):

        if crossover_type == Crossover.ORDER_CROSSOVER:
            solution = [int(x) for x in solution]
        elif crossover_type == Crossover.SINGLE_POINT_CROSSOVER:
            solution = list(numpy.argsort(solution) + 1)

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

            if init_load is not None:
                if route is None:
                    vehicles.append(chosen_vehicle.capacity)

                route = solution[solution_begin:solution_idx+1]
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

        fitness_value = -calculate_cost(routes)

        nonlocal solution_params
        if fitness_value > solution_params[1]:
            solution_params = (
                solution,
                fitness_value,
                routes,
                vehicles,
                init_loads
            )
            all_solutions.append(fitness_value)

        return fitness_value

    # Genetic algorithm
    crossover = None
    gene_space = None

    if crossover_type == Crossover.ORDER_CROSSOVER:
        crossover = order_crossover
        gene_space = list(range(1, graph.get_client_vertices_len() + 1))  # [Int]

    elif crossover_type == Crossover.SINGLE_POINT_CROSSOVER:
        crossover = one_point_crossover
        gene_space = {'low': 0, 'high': 1}  # [Float]

    chromosome_length = graph.get_client_vertices_len()
    mutation_percent_genes = (1 / chromosome_length) * 100 + 1
    mutation_type = "swap"
    keep_parents = 1
    sol_per_pop = calculate_population_size(chromosome_length)
    num_parents_mating = int(0.4 * sol_per_pop)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        on_generation=stop_at_generation,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_function,
        sol_per_pop=sol_per_pop,
        num_genes=chromosome_length,
        gene_space=gene_space,
        allow_duplicate_genes=False,
        parent_selection_type=roulette_selection,
        keep_parents=keep_parents,
        crossover_type=crossover,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes
    )

    time_start = time.time()
    ga_instance.run()

    return solution_params, all_solutions
