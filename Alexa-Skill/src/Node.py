class Node():
  def __init__(self, number, name, x, y, node_type, building, map, floor=0,):
    self.number = int(number) - 1
    self.name = name
    self.type = node_type
    self.building = building
    self.floor = floor
    self.map = map
    self.abs_x = x+ (map-1)*600
    self.x = x
    self.y = y


  def __repr__(self):
    return f"{self.name}"
