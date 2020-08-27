class Node():
  def __init__(self, number, name, x, y, node_type, building, floor=0):
    self.number = number
    self.name = name
    self.x = x
    self.y = y
    self.type = node_type
    self.building = building
    self.floor = floor

  def __repr__(self):
    return f"Node '{self.number}': '{self.name}'"

