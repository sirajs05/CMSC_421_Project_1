import sys
import time
import numpy as np
from search import Problem, astar_search
from scipy.sparse.csgraph import minimum_spanning_tree

class TSP(Problem): 

    def __init__(self, matrix):
        
        self.matrix = matrix
        self.n = matrix.shape[0]
        initial = (0,)
        super().__init__(initial)

    # Use set arithmetic to get the set of all unvisited cities
    def get_unvisited(self, state):
        
        all_cities = set(range(self.n))
        visited = set(state)
        
        return all_cities - visited
    
    # Check if every city is visited, if none left return start state, if one or more return unvisisted set
    def actions(self, state):

        if(len(state) == self.n):
            return [state[0]]
        
        unvisited = self.get_unvisited(state)

        return list(unvisited)
    
    # Appends chosen action to state, whether tour is done (simply returns state with added action of start cor there are still cities to visit
    def result(self, state, action):
        return state + (action,)
    
    # Checks of the current state is a valid goal, by checking if tour is the number of cities plus the ending start city
    # Also checks if the first city visited is the same as the last city visited
    def goal_test(self, state):
        return (len(state)  == self.n + 1) and state[0] == state[self.n]
    
    # Returns the current cost plus the edge cost of the last visited city (city we are currently at) in state 1
    # to the last city in state2 (city we are going to)
    def path_cost(self, c, state1, action, state2):
        return c + self.matrix[state1[-1], state2[-1]]
    
    # Heuristic estimating the cost remaining to complete the tour from this node
    def h(self, node):
        
        unvisited = self.get_unvisited(node.state)

        # Case 0: When only closing edge remains, no estimation needed
        if len(unvisited) == 0:
            
            return self.matrix[node.state[-1], node.state[0]]
        
        # Case 1: Exactly two edges remain, both are easy to check, so no estimation needed
        elif len(unvisited) == 1:
            
            last_city = list(unvisited)[0]
            return self.matrix[node.state[-1], last_city] + self.matrix[last_city, node.state[0]]
        
        # Case 2: MST-base estimate
        else:

            # Extract all unvisisted cities from matrix and put into submatrix for MST calculation
            unvisited_list = list(unvisited)
            size = len(unvisited_list)
            sub_matrix = np.zeros((size, size))

            for i in range(size):
                for j in range(size):
                    sub_matrix[i, j] = self.matrix[unvisited_list[i], unvisited_list[j]]

            mst = minimum_spanning_tree(sub_matrix)

            # Get sum of mst for evaluation
            return mst.sum()
        
# Load matrix, start timers, end timers when A* returns to calculate actual computing time
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Need matrix file")
        sys.exit(1)

    matrix = np.loadtxt(sys.argv[1])


    cpu_start_time = time.process_time_ns()
    wall_start_time = time.time_ns()

    problem = TSP(matrix)
    goal_node = astar_search(problem)
    goal_cost = goal_node.path_cost

    cpu_time = time.process_time_ns() - cpu_start_time
    wall_time = time.time_ns() - wall_start_time

    print(f"Final State: {goal_node}")
    print(f"Cost: {goal_cost}")
    print(f"CPU time (ns): {cpu_time}")
    print(f"Wall time (ns): {wall_time}")