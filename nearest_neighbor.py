import sys
import time
import numpy as np

def nearest_neighbor(matrix):
    
    n = matrix.shape[0]
    visited = False * n
    tour = [0]
    visited[0] = True
    current = 0

    for _ in range(n-1):
        
        best_next = None
        best_dist = float("inf")
        
        for city in range(n):
            
            if not visited[city] and matrix[current, city] < best_dist:
                best_dist = matrix[current, city]
                best_next = city
            
        tour.append(best_next)
        visited[best_next] = True
        current = best_next
    
    cost = 0
    for i in range(n):
        cost += matrix[tour[i], tour[(i+1)%n]]
    
    return tour, cost

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Need matrix file")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])

    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    tour, cost = nearest_neighbor(matrix)

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Tour: {tour}")
    print(f"Cost: {cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")