class Node():
  def __init__(self, number, name, x, y, node_type, building,map, floor=0):
    self.number = int(number) - 1
    self.name = name
    self.x = x
    self.y = y
    self.type = node_type
    self.building = building
    self.floor = floor
    self.map = map

  def __repr__(self):
    # return f"Node {self.number}: '{self.name}'"
    return f"{self.name}"
