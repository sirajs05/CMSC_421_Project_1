import sys
import time
import numpy as np
from nearest_neighbor import nearest_neighbor

def nearest_neighbor_2opt(matrix):

    tour, cost = nearest_neighbor(matrix)
    n = len(tour)
    
    improved = True
    while improved:
        
        improved = False
        for i in range(n):
            
            next_i = (i+1) % n
            
            test_tour = tour.copy()
            test_tour[i], test_tour[next_i] = tour[next_i], tour[i]

            test_cost = 0
            for j in range(n):
                test_cost += matrix[test_tour[j], test_tour[(j+1)%n]]
            
            if test_cost < cost:
                tour = test_tour
                cost = test_cost
                improved = True
                break


    return tour, cost

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Need matrix file")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = nearest_neighbor_2opt(matrix)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")