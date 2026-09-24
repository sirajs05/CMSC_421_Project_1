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

    def get_unvisited(self, state):
        
        all_cities = set(range(self.n))
        visited = set(state)
        
        return all_cities - visited
    
    def actions(self, state):

        if(len(state) == self.n):
            return [state[0]]
        
        unvisited = self.get_unvisited(state)

        return list(unvisited)
    
    def result(self, state, action):
        return state + (action,)
    
    def goal_test(self, state):
        return (len(state)  == self.n + 1) and state[0] == state[self.n]
    
    def path_cost(self, c, state1, action, state2):
        return c + self.matrix[state1[-1], state2[-1]]
    
    def h(self, node):
        
        unvisited = self.get_unvisited(node.state)

        if len(unvisited) == 0:
            
            return self.matrix[node.state[-1], node.state[0]]
        
        elif len(unvisited) == 1:
            
            last_city = list(unvisited)[0]
            return self.matrix[node.state[-1], last_city] + self.matrix[last_city, node.state[0]]
        
        else:

            unvisited_list = list(unvisited)
            size = len(unvisited_list)
            sub_matrix = np.zeros((size, size))

            for i in range(size):
                for j in range(size):
                    sub_matrix[i, j] = self.matrix[unvisited_list[i], unvisited_list[j]]

            mst = minimum_spanning_tree(sub_matrix)

            return mst.sum()
        
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