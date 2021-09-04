import time

SUCCESS = True
FAILURE = False
GOALSTATE = "012345678"

# Node class ->
class Node:
    parent = None
    children = []
    grid = None
    direction = None
    depth = 0
    path_cost = 0
    estimated_cost = 0

    def __init__(self, grid, direction, depth):
        self.grid = grid
        self.direction = direction
        self.depth = depth
        # path_cost equals depth -as the cost of every edge is equal to 1-
        self.path_cost = depth 

    def add_child(self, node):
        self.children.append(node)
        node.parent = self
    
    # Printing node
    def print_node(self):
        print(self.direction)
        for i in range(0, 9, 3):
            print(self.grid[i], self.grid[i+1], self.grid[i+2])

    # in each function of the four functions:
    # check first if it is a legal move -> if true apply the move and if false return None
    def move_to_up(self, g, i):
        if i-3 >= 0:
            newgrid = list(g)
            newgrid[i] = newgrid[i-3]
            newgrid[i-3] = '0'
            g = ''.join(newgrid)
            return Node(g,'Up',self.depth+1)
        return None

    def move_to_down(self, g, i):
        if i+3 < 9:
            newgrid = list(g)
            newgrid[i] = newgrid[i+3]
            newgrid[i+3] = '0'
            g = ''.join(newgrid)
            return Node(g,'Down',self.depth+1)
        return None
        
    def move_to_left(self, g, i):
        if i%3 > 0:
            newgrid = list(g)
            newgrid[i] = newgrid[i-1]
            newgrid[i-1] = '0'
            g = ''.join(newgrid)
            return Node(g,'Left',self.depth+1)
        return None

    def move_to_right(self, g, i):
        if i%3 < 2:
            newgrid = list(g)
            newgrid[i] = newgrid[i+1]
            newgrid[i+1] = '0'
            g = ''.join(newgrid)
            return Node(g,'Right', self.depth+1)
        return None

    # expanding each node with the possible movements in each of the four directions
    def expand_node(self):
        zeroPostion = self.grid.index('0')
                        
        Up = self.move_to_up(self.grid, zeroPostion)
        if Up!=None:
            # if the up node not equal none so add it to the node's children
            self.add_child(Up)

        Down = self.move_to_down(self.grid, zeroPostion)
        if Down!=None:
            # if the down node not equal none so add it to the node's children
            self.add_child(Down)
        
        Left = self.move_to_left(self.grid, zeroPostion)
        if Left!=None:
            # if the left node not equal none so add it to the node's children
            self.add_child(Left)

        Right = self.move_to_right(self.grid, zeroPostion)
        if Right!=None:
            # if the right node not equal none so add it to the node's children
            self.add_child(Right)

# -------------------------------------------------------------------------------------------------------------

# gameGraph class ->
class gameGraph:
    solution_path = []
    nodes_expanded = 0
    running_time = None

    def __init__(self):
        pass
    
    def is_solvable(self, grid):
        # number of inversions -> 
        # A pair of tiles their values are in reverse order of their appearance in goal state.
        inv_count = 0 
        for i in range(8):
            for j in range(i+1, 9):
                if grid[j]!='0' and grid[i]>grid[j]:
                    inv_count += 1

        return (inv_count % 2 == 0)

    # Tracing backwards to find the path between the root and the goal
    def path_trace(self, node):
        path = []
        path.append(node)
        while node.parent != None:
            node = node.parent
            path.append(node)
        path.reverse()
        return path

    # Printing path between intial state and the goal
    def print_solution(self):
        for step in self.solution_path:
            print("Step", step.depth, ': ', end='') 
            step.print_node()
            print("_________________________________")
        print("cost_of_path =", self.solution_path[-1].path_cost)
        print("nodes_expanded =", self.nodes_expanded)
        print("search_depth =", self.solution_path[-1].depth)
        print("running_time =", self.running_time, "ms")
    
    def BFS(self, intialState): 
        start = time.time()
        intialNode = Node(intialState, 'Intial state', 0)
        self.adj_list = [intialNode]
        frontier = [intialNode]
        explored = set()

        if self.is_solvable(intialState):
            while len(frontier) != 0:
                state = frontier.pop(0)
                explored.add(state.grid)

                if GOALSTATE == state.grid:
                    self.running_time = (time.time() - start)* 10**3
                    self.nodes_expanded = len(explored) - 1
                    self.solution_path = self.path_trace(state)
                    return SUCCESS
                    
                state.expand_node()
                
                for child in state.children:
                    if child not in frontier and child.grid not in explored:
                        frontier.append(child)

        return FAILURE
    
# ..................................................................................................
# "640372815"
G = gameGraph()
solution_found = G.BFS("125348067")
if solution_found:
   G.print_solution() # visualization

