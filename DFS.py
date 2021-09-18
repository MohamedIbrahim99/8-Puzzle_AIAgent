
class node:
  grid= None
  emptytilindex= None
  parent= None
  children= []
  def addChild(self, node):
      self.children.append(node)
      node.parent = self
  def __init__(self,state, x):
    self.grid=state
    self.emptytilindex=x
  def printNode(self):
    for i in range(0,9,3):
      print (self.grid[i],self.grid[i+1],self.grid[i+2])

def dfs(start, end):
  #processing in input to get the start node and end node
  startnode=node(start, start.index('0'))
  endnode=node(end, end.index('0'))
  
  frontier=[startnode] #contains nodes
  explored=set() #contains grids
 

  while len(frontier) != 0:
    state= frontier[-1]
    frontier.pop(-1)
    explored.add(state.grid)

 
    if state.grid==endnode.grid:
      getpath(state)
      return "success" #goal path function call
    
    #create chiled nodes function
    ch1,ch2,ch3,ch4= moveup(state),movedown(state),moveright(state),moveleft(state)


    #add them to frontier if they not on explored or frontier
    if (ch4 == None):
      var=None
    else:
      if (ch4 not in frontier and ch4.grid not in explored):
        frontier.append(ch4)

      

    if (ch3 == None):
      var=None
    else:
      if (ch3 not in frontier and ch3.grid not in explored):
        frontier.append(ch3)


    if (ch2 == None):
      var=None
    else:
      if (ch2 not in frontier and ch2.grid not in explored):
        frontier.append(ch2)


    if (ch1 == None):
      var=None
    else:
      if (ch1 not in frontier and ch1.grid not in explored):
        frontier.append(ch1)
 
  return "failure"

def moveup(state):
  child = node(state.grid,state.emptytilindex) #create new node function call duplicate for the state input
  index = state.emptytilindex #get the index of 0 in the state input
 
  if index not in [0,1,2]:
    child.emptytilindex=index-3
    arr=list(child.grid)
    arr[index-3],arr[index]='0',arr[index-3]
    child.grid="".join(arr)
    state.addChild(child)
    return child
  else:
    return None  
 
 
def movedown(state):
  child =node(state.grid,state.emptytilindex) #create new node function call duplicate for the state input
  index = state.emptytilindex #get the index of 0 in the state input
 
  if index not in [6,7,8]:
    child.emptytilindex=index+3
    arr=list(child.grid)
    arr[index+3],arr[index]='0',arr[index+3]
    child.grid="".join(arr)
    state.addChild(child)
    return child
  else:
    return None  
 
def moveright(state):
  child =node(state.grid,state.emptytilindex) #create new node function call duplicate for the state input
  index = state.emptytilindex #get the index of 0 in the state input
 
  if index not in [2,5,8]:
    child.emptytilindex=index+1
    arr=list(child.grid)
    arr[index+1],arr[index]='0',arr[index+1]
    child.grid="".join(arr)
    state.addChild(child)
    return child
  else:
    return None  
 
 
def moveleft(state):
  child =node(state.grid,state.emptytilindex) #create new node function call duplicate for the state input
  index = state.emptytilindex #get the index of 0 in the state input
 
  if index not in [0,3,6]:
    child.emptytilindex=index-1
    arr=list(child.grid)
    arr[index-1],arr[index]='0',arr[index-1]
    child.grid="".join(arr)
    state.addChild(child)
    return child
  else:
    return None

def getpath(state):
  array=[state]
  while (state.parent!=None):
    state=state.parent
    array.append(state)
  array.reverse()
  for i in range (len(array)):
    print (array[i].printNode())
    
  print ("path cost = ", len(array)-1)
