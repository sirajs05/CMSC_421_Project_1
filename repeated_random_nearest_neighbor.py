import sys
import time
import numpy as np
import random
from  nearest_neighbor_2opt import two_opt

# Unlike Nearest Neighbor that greedily selects the closest city, greedily
# Randomly pick one of k closest cities, each of the num_repeats independent randomized constructions is refined by 2-Opt
def repeated_random_nearest_neighbor(matrix, k, num_repeats):

    n = matrix.shape[0]

    # Save the best tour, and cost across all repeats
    best_tour = None
    best_cost = float("inf")

    for _ in range(num_repeats):
    
        # Each repeat builds a new tour to test
        visited = [False] * n
        tour = [0]
        visited[0] = True
        current = 0
    
        for _ in range(n-1):

            # Get every unvisited city along with its distance
            # Rebuilt every step because of different tours and different choices
            candidates = []
    
            for city in range(n):
                if not visited[city]:
                    candidates.append((city, matrix[current, city]))

            # Get actual cost by destructing pair, then pick smallest k pairs, randomly choose one
            candidates.sort(key=lambda pair: pair[1])
            k_check = min(k, len(candidates))
            k_closest = candidates[:k_check]
            best_next, _ = random.choice(k_closest)

            # Add to tour
            tour.append(best_next)
            visited[best_next] = True
            current = best_next

        # Get cost
        cost = 0
        for j in range(n):
            cost += matrix[tour[j], tour[(j+1) % n]]

        # Refine tour
        tour, cost = two_opt(matrix, tour, cost)

        # Check if tour is better than current best
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost

# Load matrix, start timers, end timers when Repeated Randomness Nearest Neighbors returns to calculate actual computing time
if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Need matrix file, k hyperparameter, and num_repeated hyperparameter")
        sys.exit(1)

    # Get matrix, enforce types to put in as args
    matrix = np.loadtxt(sys.argv[1])
    k = int(sys.argv[2])
    num_repeats = int(sys.argv[3])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = repeated_random_nearest_neighbor(matrix, k, num_repeats)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")