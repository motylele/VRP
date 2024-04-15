import numpy
import pygad


def genetic_algorithm(graph):

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

    # Creating route, adding warehouses to both ends
    def create_route(route, warehouse):
        return [warehouse.index] + list(route) + [warehouse.index]

    # Fitness function calculating solution fitness value
    def fitness_function(ga_instance, solution, solution_id):
        solution = [int(x) for x in solution]

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
            else: # init_load == 0
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

        return -calculate_cost(routes) #, (routes, vehicles, init_loads)

    # Genetic algorithm

    sol = graph.get_vertices_permutation()
    print(sol)
    num_generations = 50
    num_parents_mating = 4
    sol_per_pop = 8
    num_genes = len(sol)
    gene_space = list(range(1, len(sol) + 1))
    parent_selection_type = "sss"
    keep_parents = 1
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           gene_space=gene_space,
                           allow_duplicate_genes=False,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes)

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

    # Accessing the extra information returned by the fitness function
    # extra_info = solution_fitness[1]
    # print("Extra information: ", extra_info)
