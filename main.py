class Node:
  def __init__(self, name=None, floor=0, dept=None):
    self.name = name
    self.floor = floor
    self.dept = dept

# Constraint: Each cell must have at most one node.
n= 300 # 600m/2 not fixed
m= 75 # 150m/2 not fixed

arr = [Node() for i in range(m) for j in range(n)]

# Create array with req nodes/corridors/blah


currNode = Node()
#initialize node with current location


# Receive input from Alexa about where user wants to go
dest = None

# Apply A* to get closest dist.



