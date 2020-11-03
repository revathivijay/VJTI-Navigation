import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import json
from Node import Node

def initialize_map(filename):
    f = open(filename)
    data = json.load(f)
    nodes = {}
    map_node = {}
    for key, node in data.items():
        temp_node = Node(
            number=node["Node number"], ## dont change this to -1
            name=node["Node Name"],
            x=int(node["x_pos"]),
            y=int(node["y_pos"]),
            node_type=node["Type"],
            floor=int(node["Floor"]),
            building=node["Building"],
            map = int(node["Map Number"])
        )
        nodes[int(key)-1] = temp_node
        map_node[node["Node Name"]] = int(node["Node number"])-1
    return nodes,map_node

nodes, _ = initialize_map("nodes.json")
img = Image.open('resized-new/1-0.jpg')
fig,a = plt.subplots(2,2)
a[0][0].imshow(img)
for i in range(len(nodes)):
    if(nodes[i].map==1):
        a[0][0].plot(nodes[i].x, nodes[i].y, 'o')
        a[0][0].text(nodes[i].x+20, nodes[i].y, i
                 +1)
img = Image.open('resized-new/2-0.jpg')
a[0][1].imshow(img)
for i in range(len(nodes)):
    if(nodes[i].map==2 and nodes[i].floor==0):
        a[0][1].plot(nodes[i].x, nodes[i].y, 'o')
        a[0][1].text(nodes[i].x+20, nodes[i].y, i
                 +1)
img = Image.open('resized-new/3-0.jpg')
a[1][0].imshow(img)
for i in range(len(nodes)):
    if(nodes[i].map==3 and nodes[i].floor==0):
        a[1][0].plot(nodes[i].x, nodes[i].y, 'o')
        a[1][0].text(nodes[i].x+20, nodes[i].y, i
                 +1)
img = Image.open('resized-new/3-1.jpg')
a[1][1].imshow(img)
for i in range(len(nodes)):
    if(nodes[i].map==3 and nodes[i].floor==1):
        a[1][1].plot(nodes[i].x, nodes[i].y, 'o')
        a[1][1].text(nodes[i].x+20, nodes[i].y, i
                 +1)

plt.show()