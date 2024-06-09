from Descent import descent_algorithm
import time


# Multistart descent algorithm
def multistart_descent(graph, num_iterations, time_limit, neighborhood_type):

    all_solutions = []
    best_descent_instance = None
    min_value = float('inf')

    start_time = time.time()
    for i in range(num_iterations):
        if time.time() - start_time >= time_limit:
            break

        descent_instance = descent_algorithm(
            graph,
            neighborhood_type=neighborhood_type
        )
        current_value = descent_instance[1]

        if current_value < min_value:
            min_value = current_value
            best_descent_instance = descent_instance
            all_solutions.append(current_value)

    return best_descent_instance, all_solutions
