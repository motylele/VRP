import pygad
import numpy

def roulette_mutation(offspring, ga_instance):
    return offspring

def order_crossover(parents, offspring_size, ga_instace):
    offspring = []

    for i in range(offspring_size[0]):
        parent1 = parents[i % parents.shape[0], :]
        parent2 = parents[(i + 1) % parents.shape[0], :]

        split_point1, split_point2 = sorted(numpy.random.choice(range(offspring_size[1]), size=2, replace=False))


    return numpy.array(offspring)
def one_point_crossover(parents, offspring_size, ga_instance):
    offspring = []

    for i in range(offspring_size[0]):
        parent1 = parents[i % parents.shape[0], :]
        parent2 = parents[(i + 1) % parents.shape[0], :]

        split_point = numpy.random.choice(range(offspring_size[1]))

        parent1[split_point:] = parent2[split_point:]

        offspring.append(parent1)

    return numpy.array(offspring)

def fitness_func(ga_instance, solution, solution_idx):
    output = numpy.sum(solution * equation_inputs)
    fitness = 1.0 / (numpy.abs(output - desired_output) + 0.000001)
    return fitness

equation_inputs = [4,-2,3.5]
desired_output = 44

ga_instance = pygad.GA(num_generations=10,
                       sol_per_pop=5,
                       num_parents_mating=2,
                       num_genes=len(equation_inputs),
                       fitness_func=fitness_func,
                       crossover_type=order_crossover)

ga_instance.run()