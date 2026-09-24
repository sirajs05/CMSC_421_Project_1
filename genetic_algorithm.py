import sys 
import time
import random
import numpy as np


def order_crossover(parent1, parent2):
    
    n = len(parent1)

    cut1, cut2 = random.sample(range(1,n+1), 2)
    cut1, cut2 = min(cut1, cut2), max(cut1, cut2)
    child = [None]*n
    child[cut1:cut2] = parent1[cut1:cut2]

    fill_positions = list(range(cut2, n)) + list(range(0, cut1))
    read_order = list(range(cut2, n)) + list(range(0, cut2))

    fill_idx = 0
    read_idx = 0

    while fill_idx < len(fill_positions):

        value = parent2[read_order[read_idx]]

        if value not in child:
            child[fill_positions[fill_idx]] = value
            fill_idx += 1

        read_idx += 1

    return child

def genetic_algorithm(matrix, mut_chance, pop_size, num_gens):

    n = matrix.shape[0]
    population = []

    for _ in range(pop_size):
        population.append(random.sample(range(n), n))

    for gen in range(num_gens):
        children = []

        for _ in range(pop_size):
            parent1_idx, parent2_idx = random.sample(range(pop_size), 2)
            parent1, parent2 = population[parent1_idx], population[parent2_idx]

            child = order_crossover(parent1, parent2)

            probability_check = random.random()

            if(probability_check < mut_chance):
        
                node1, node2 = random.sample(range(n), 2)
                child[node1], child[node2] = child[node2], child[node1]
            
            children.append(child)

        combined = population + children

        scored = []

        for tour in combined:

            cost = 0
            for j in range(n):
                cost += matrix[tour[j], tour[(j+1)%n]]
            scored.append((tour, cost))

        scored.sort(key=lambda pair: pair[1])

        population = [pair[0] for pair in scored[:pop_size]]
        best_tour, best_cost = scored[0]

    return best_tour, best_cost

if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        print("Need matrix file, and hyperparamter mutation chance, population, and number of generations")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])
    mut_chance = float(sys.argv[2])
    pop_size = int(sys.argv[3])
    num_gens = int(sys.argv[4])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = genetic_algorithm(matrix, mut_chance, pop_size, num_gens)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")