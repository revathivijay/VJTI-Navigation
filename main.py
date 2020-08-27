import json 
from Node import Node

# Initialize Map
def initialize_map(filename): 
    f = open(filename) 
    data = json.load(f) 
    nodes = []
    for _,node in data.items(): 
      temp_node = Node(
        number = node["number"],
        name = node["name"],
        x = node["x"],
        y = node["y"],
        node_type = node["type"],
        floor = node["floor"],
        building = node["building"]
      )
      nodes.append(temp_node)
    return nodes
  

if __name__ == "__main__":
    dump_file = 'nodes.json'
    nodes = initialize_map(dump_file)
    # Initialize Source/Destination Nodes
    # Call Dijikstra/A* to get sequence of nodes
    # Call Directions Function 
    # return directions output





