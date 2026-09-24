import sys
import time
import numpy as np
import random
from  nearest_neighbor_2opt import two_opt

def repeated_random_number_neighbor(matrix, k, num_repeats):

    n = matrix.shape[0]

    best_tour = None
    best_cost = float("inf")

    for _ in range(num_repeats):
    
        visited = [False] * n
        tour = [0]
        visited[0] = True
        current = 0
    
        for _ in range(n-1):

            candidates = []
    
            for city in range(n):
                if not visited[city]:
                    candidates.append((city, matrix[current, city]))

            candidates.sort(key=lambda pair: pair[1])
            k_check = min(k, len(candidates))
            k_closest = candidates[:k_check]
            best_next, _ = random.choice(k_closest)

            tour.append(best_next)
            visited[best_next] = True
            current = best_next

        cost = 0
        for j in range(n):
            cost += matrix[tour[j], tour[(j+1) % n]]

        tour, cost = two_opt(matrix, tour, cost)

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Need matrix file, k hyperparameter, and num_repeated hyperparameter")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])
    k = int(sys.argv[2])
    num_repeats = int(sys.argv[3])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = repeated_random_number_neighbor(matrix, k, num_repeats)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")