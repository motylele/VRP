import time


def simulated_annealing(graph, num_iterations, time_limit, initial_temperature, final_temperature, neighborhood_type):
    beta = (initial_temperature - final_temperature) / ((num_iterations -1) * initial_temperature * final_temperature)

    start_time = time.time()
    for i in range(num_iterations):
        if time.time() - start_time >= time_limit:
            break

        # acceptance_probability
    print("SIMULATED ANNEALING")