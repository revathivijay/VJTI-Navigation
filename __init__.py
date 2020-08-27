import csv
import json 
from Node import Node

def create_adj_list(input_file):

    adj_list = {}

    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                adj_list[row['Node ']].add(row['Adjacents'])
            except KeyError:
                adj_list[row['Node ']] = {row['Adjacents']}
            try:
                adj_list[row['Adjacents']].add(row['Node '])
            except KeyError:
                adj_list[row['Adjacents']] = {row['Node ']}

    return adj_list


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
    csv_file = 'edges.csv'
    adj_list = create_adj_list(csv_file) 
    print(adj_list)
    # Initialize Source/Destination Nodes
    # Call Dijikstra/A* to get sequence of nodes
    # Call Directions Function 
    # return directions output


