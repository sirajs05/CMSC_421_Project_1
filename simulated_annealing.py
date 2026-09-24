import sys
import time
import math
import random
import numpy as np

def simulated_annealing(matrix, alpha, init_temp, max_iters):
    
    n = matrix.shape[0]
    current_tour = random.sample(range(n), n)
    t = init_temp

    for _ in range(max_iters):
        
        node1, node2 = random.sample(range(n), 2)
        candidate_tour = current_tour.copy()
        candidate_tour[node1], candidate_tour[node2] = current_tour[node2], current_tour[node1]

        current_cost = 0
        for j in range(n):
            current_cost += matrix[current_tour[j], current_tour[(j+1)%n]]

        candidate_cost = 0
        for j in range(n):
            candidate_cost += matrix[candidate_tour[j], candidate_tour[(j+1)%n]]

        candidate_accept = False

        if candidate_cost < current_cost:

            current_cost = candidate_cost
            current_tour = candidate_tour
            candidate_accept = True

        else:

            score = 1 / current_cost
            score_prime = 1 / candidate_cost
            probability_func = math.exp((score_prime - score) / t)
            
            if random.random() < probability_func:

                current_cost = candidate_cost
                current_tour = candidate_tour
                candidate_accept = True

        if candidate_accept:
            t = t * alpha


    return current_tour, current_cost

if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        print("Need matrix file, and hyperparamter alpha, initial temp, and max iterations")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])
    alpha = float(sys.argv[2])
    init_temp = float(sys.argv[3])
    max_iters = int(sys.argv[4])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = simulated_annealing(matrix, alpha, init_temp, max_iters)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")