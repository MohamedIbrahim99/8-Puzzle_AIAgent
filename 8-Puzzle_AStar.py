import numpy as np
import heapq
import math
from copy import deepcopy 

class Node:
    children = np.array([])
    parent = None
    path_cost = 0
    estimated_cost = 0
    state = []
    depth = 0
    def __lt__(self, other):
        return self.depth > other.depth
    def __le__(self, other):
        return self.depth > other.depth

    
class Main:
    def __init__(self) :
        self.no_expanded_nodes = 0
        
    # main function
    def solve_A_Star(self, initial_node , heuristic_type):
        self.no_expanded_nodes = 0
        if heuristic_type == "Euclidean":
            solution_node = self.A_star(initial_node, self.Heuristic_Euclidean)
        else:
            solution_node = self.A_star(initial_node, self.Heuristic_Manhattan)
        path = self.pathTrace(solution_node)
        self.printPath(path, heuristic_type)
        return

     # A* algorithm
    def A_star(self , initial_node, heuristic_func):
        pq = []
        state = initial_node.state 
        cost = self.calculate_Heuristic(state , heuristic_func)
        initial_node.estimated_cost = cost
        heapq.heappush(pq , (cost,initial_node))
        explored = []
        while pq:
            c,node = heapq.heappop(pq)
            explored.append(node.state)
            if (self.goal_test(node.state)):
                return node
            self.expand(node)
            for child in node.children:
                # if neighbor in frontier
                flag = 0
                j = 0
                for co,no in pq:
                    if np.array_equal(child.state , no.state):
                        if (child.estimated_cost < co):
                            # update the priority
                            pq[j] = (child.estimated_cost, child)
                            heapq.heapify(pq)
                        flag = 1
                        break
                    j += 1
                # if neighbor not in explored & not in frontier
                if flag == 0:
                    flag2 = 0
                    for e in explored:
                        if np.array_equal(child.state , e):
                            flag2 = 1
                            break
                    if flag2 == 0 :
                        cost = child.path_cost + self.calculate_Heuristic(child.state , heuristic_func)
                        child.estimated_cost = cost
                        heapq.heappush(pq , (cost,child))
        return None

    # Higher order function to calculate the heuristic
    # take the hueristic function as attribute and use it
    def calculate_Heuristic(self,state , heuristic_func):
        h = 0 
        goal_coordinates = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
        for i in range(0,3):
            for j in range(0,3):
                x = state[i][j]
                if x == 0:
                    continue
                h += heuristic_func(i, j , goal_coordinates[x])
        return h

    # calculate the Manhattan Heuristic
    def Heuristic_Manhattan(self ,i, j , goal_coordinates):
        return abs(i - goal_coordinates[0]) + abs(j - goal_coordinates[1])

    # calculate the Euclidean Heuristic
    def Heuristic_Euclidean(self, i, j , goal_coordinates):
        return math.sqrt( (i - goal_coordinates[0])**2 + (j - goal_coordinates[1])**2 )


    # test if this state is the goal state 
    def goal_test(self , state):
        if (np.array_equal( state , np.array([[0,1,2],[3,4,5],[6,7,8]]) )):
            return True
        return False

    # expand the node with the possible movements in each of the four directions
    def expand(self , node):
        empty_space = np.argwhere(node.state == 0)
        # the possible up and down moves
        if (empty_space[0][0] != 0):
            # up case
            newNode2 = self.create_child(node)
            newNode2.state[empty_space[0][0]][empty_space[0][1]] = newNode2.state[empty_space[0][0]-1][empty_space[0][1]]
            newNode2.state[empty_space[0][0]-1][empty_space[0][1]] = 0
            self.no_expanded_nodes += 1
        if (empty_space[0][0] != 2):
            # down case
            newNode1 = self.create_child(node)
            newNode1.state[empty_space[0][0]][empty_space[0][1]] = newNode1.state[empty_space[0][0]+1][empty_space[0][1]]
            newNode1.state[empty_space[0][0]+1][empty_space[0][1]] = 0
            self.no_expanded_nodes += 1

        # the possible right and left moves
        if (empty_space[0][1] != 0):
            # left case
            newNode3 = self.create_child(node)
            newNode3.state[empty_space[0][0]][empty_space[0][1]] = newNode3.state[empty_space[0][0]][empty_space[0][1]-1]
            newNode3.state[empty_space[0][0]][empty_space[0][1]-1] = 0
            self.no_expanded_nodes += 1
        if (empty_space[0][1] != 2):
            # right case
            newNode4 = self.create_child(node)
            newNode4.state[empty_space[0][0]][empty_space[0][1]] = newNode4.state[empty_space[0][0]][empty_space[0][1]+1]
            newNode4.state[empty_space[0][0]][empty_space[0][1]+1] = 0
            self.no_expanded_nodes += 1
            
        return

    # create a child and and edit his attributes
    def create_child(self, parent):
        child = Node()
        child.parent = parent
        child.depth = parent.depth + 1
        child.path_cost = parent.path_cost + 1
        child.state = deepcopy(parent.state)
        parent.children = np.append(parent.children , child)
        return child

    # Tracing backwards to find the path between the root and the goal
    def pathTrace(self, node):
        path = []
        path.append(node)
        while node.parent != None:
            node = node.parent
            path.append(node)
        path.reverse()
        return path

    # Printing path between intial state and the goal
    def printPath(self, path , heuristic_type):
        k = 0
        for step in path:
            print("Step", k, ':') 
            k += 1
            self.print_node(step)
            print("_________________________________")
        print("The Heuristic Type : ",heuristic_type)
        print("Number of Expanded Nodes : " , self.no_expanded_nodes)
        return

    # Printing node
    def print_node(self, node):
        for i in range(0,3):
            for j in range(0,3):
                print(node.state[i][j],end = "  ") 
            print()
        return
    
    # convert the string input to 2d array
    def string_to_2dArray(self, state):
        arr = []
        x = []
        i = 0
        for d in state:
            if (d.isdigit()):
                arr.append(int(d))
        arr = np.reshape(arr, (3, 3))
        return arr

# ..................................................................................................

# Instance of Class Main
Object = Main()
initial = Node()
initial.state = Object.string_to_2dArray("1,0,2,7,5,4,8,6,3")
Object.solve_A_Star(initial ,"Euclidean")

#initial.state = np.array([[1,2,5],[3,4,8],[6,7,0]])
# Manhattan
# Euclidean