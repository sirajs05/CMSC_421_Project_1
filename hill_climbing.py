import sys
import time
import random
import numpy as np

def hill_climbing(matrix, num_restarts):
    
    n = matrix.shape[0]
    best_tour = None
    best_cost = float("inf")

    for _ in range(num_restarts):

        random_perm_list = random.sample(list(range(n)), n)
        
        no_improvement_count = 0
        max_no_improvement = n * 10

        while no_improvement_count < max_no_improvement:

            node1, node2 = random.sample(range(n), 2)

            test_list = random_perm_list.copy()
            test_list[node1], test_list[node2] = random_perm_list[node1], random_perm_list[node2]

            current_cost = 0
            for j in range(n):
                current_cost += matrix[random_perm_list[j], random_perm_list[(j+1)%n]]

            test_cost = 0
            for j in range(n):
                test_cost += matrix[test_list[j], test_list[(j+1)%n]]

            if test_cost < current_cost:
                
                random_perm_list = test_list
                no_improvement_count = 0

            else:
                no_improvement_count += 1
        

        current_cost = 0
        for j in range(n):
            current_cost += matrix[random_perm_list[j], random_perm_list[(j+1)%n]]

        if(best_cost > current_cost):
            best_tour = random_perm_list
            best_cost = current_cost
    
    return best_tour, best_cost

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Need matrix file, and hyperparamter num_restarts")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])
    num_restarts = int(sys.argv[2])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = hill_climbing(matrix, num_restarts)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")