import sys
import time
import math
import random
import numpy as np

# Start with random permutation of tour, accept candidates if better, or if worse check against probability function
# max_iters is the number of times this loop runs to get close to best tour and cost
def simulated_annealing(matrix, alpha, init_temp, max_iters):
    
    # Start with random tour, generated once
    n = matrix.shape[0]
    current_tour = random.sample(range(n), n)
    t = init_temp

    for _ in range(max_iters):
        
        # Create neighbor by swapping two cities in current tour
        node1, node2 = random.sample(range(n), 2)
        candidate_tour = current_tour.copy()
        candidate_tour[node1], candidate_tour[node2] = current_tour[node2], current_tour[node1]

        # Get current cost and candidate cost
        current_cost = 0
        for j in range(n):
            current_cost += matrix[current_tour[j], current_tour[(j+1)%n]]

        candidate_cost = 0
        for j in range(n):
            candidate_cost += matrix[candidate_tour[j], candidate_tour[(j+1)%n]]

        # if candidate cost is better accept
        candidate_accept = False

        if candidate_cost < current_cost:

            current_cost = candidate_cost
            current_tour = candidate_tour
            candidate_accept = True

        # If candidate is not better, generate probability acceptance based on cost and temp
        else:

            probability_func = math.exp((current_cost - candidate_cost) / t)
            
            if random.random() < probability_func:

                current_cost = candidate_cost
                current_tour = candidate_tour
                candidate_accept = True

        # If candidates are accepted (better or worse) cool down temp via alpha
        if candidate_accept:
            t = t * alpha


    return current_tour, current_cost

# Load matrix, start timers, end timers when The Genetic Algorithm (Order Crossover) returns to calculate actual computing time
if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        print("Need matrix file, and hyperparamter alpha, initial temp, and max iterations")
        sys.exit(1)

    # Get all args, enforce types
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