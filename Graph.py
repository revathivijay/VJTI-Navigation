from collections import defaultdict
import sys
from Heap import Heap
import csv
import json
import re
from Node import Node
from math import sqrt
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import PIL

"""
{0: Main Gate , 1: , 2: Main Building Entrace, 3: , 4: Main Building Staircase, 5: Director's Office,
6: Lab 3, 7: Dep1 , 8: Dep2 , 9: , 10: Computer Department, 11: Study Space , 12: , 13: AL004 ,
14: , 15: Stage , 16: , 17: Audi Entrance, 18: Stage Washroom, 19: Canteen Quad Entrance,
20: Quad , 21: Quad Steps, 22: , 23: , 24: , 25: , 26: CCF1, 27: Library,
28: Library Staircase, 29: COE, 30: , 31: Electrical Dept/Staircase, 32: Statue, 33: Quad Entrance}
"""

## for viusalizing
# pixel_mapping = {
#     0: (337,448),
#     1: (337,409),
#     2: (395,409),
#     3: (471,409),
#     4: (540,409),
#     5: (540,267),
#     6: (491,276),
#     7: (491,262),
#     8: (426,276),
#     9: (426,216),
#     10: (426,128),
#     11: (460,128),
#     12: (338,128),
#     13: (240,127),
#     14: (240,216),
#     15: (337,216),
#     16: (337,276),
#     17: (240,276),
#     18: (240,325),
#     19: (240,409),
#     20: (198,409),
#     21: (122,448),
#     22: (58,448),
#     23: (58,409),
#     24: (540,128),
# }
#

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
            node_type=node["Type "],
            floor=int(node["Floor"]),
            building=node["Building"],
            map = node["Map Number"]
        )
        nodes[int(key)-1] = temp_node
        map_node[node["Node Name"]] = int(node["Node number"])-1
    return nodes,map_node

"""
def get_node_mapping(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        map_nodes = {}
        for row in csv_reader:
            map_nodes[row['Node']]  = int(row['Node Number'])-1
    return map_nodes
"""

class Graph():

    def __init__(self, V, nodes):
        self.V = V
        self.graph = defaultdict(list)
        self.nodes = nodes

    def calculateDistance(self, src, dest):
        return sqrt(pow(self.nodes[src].x - self.nodes[dest].x, 2)+pow(self.nodes[src].y-self.nodes[dest].y, 2))

    def addEdge(self, src, dest):
        weight = self.calculateDistance(src, dest)
        # print(src, dest, weight)
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

    def addAllEdges(self, input_file):
        with open(input_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.addEdge(int(row['Nodes'])-1, int(row['Adjacents'])-1)

    def getPath(self, parent, j, path):
        if parent[j] == -1 :
            return
        self.getPath(parent , parent[j], path)
        # print (j, "\t", self.nodes[j].name)
        path.append(j)


    def getSolution(self, dist, parent, source, dest):
        # print("Vertex \t\tDistance from Source\tPath")
        path = []
        path.append(source)
        self.getPath(parent, dest, path)
        print()
        return path

    def getDirections(self, path, dest):
        directions = []
        directions_text = ""
        # print("In directions: ", path)
        for i in range(1, len(path)):
            ## case 1: for first node - only parent is considered
            if i==1:
                curr = path[i]
                prev = path[i-1]
                if self.nodes[curr].x > self.nodes[prev].x and self.nodes[curr].y == self.nodes[prev].y:
                    directions.append('Right')
                elif self.nodes[curr].x < self.nodes[prev].x and self.nodes[curr].y == self.nodes[prev].y:
                    directions.append('Left')
                elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y > self.nodes[prev].y:
                    directions.append('Straight')
                elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y < self.nodes[prev].y:
                    directions.append('Back')
                else:

                    directions.append("check em")
                if(directions[-1]!='Straight'):
                    directions_text = "First turn {} and keep walking".format(directions[-1])
                else:
                    directions_text = "Walk straight"
                if(self.nodes[curr].name!=""):
                    directions_text+= " till you reach " + self.nodes[curr].name+"."
                else:
                    directions_text+="."

            else:
                x1 = self.nodes[path[i-2]].x            # x1,y1 -> x2,y2
                y1 = self.nodes[path[i-2]].y
                x2 = self.nodes[path[i-1]].x
                y2 = self.nodes[path[i-1]].y
                x3 = self.nodes[path[i]].x
                y3 = self.nodes[path[i]].y

                # Very special case of mech building passage which is slant.
                if (path[i - 1] in range(33, 40) and path[i] in range(34, 41)) or (path[i-1] in range(48,52) and path[i] in range(48,52)):
                    if (path[i - 1] == 33):
                        directions.append('Slight right')
                    else:
                        directions.append('Straight')

                elif nodes[path[i-1]].name=='staircase' and nodes[path[i]].name == 'staircase' and nodes[path[i]].floor != nodes[path[i-1]].floor:
                    floor = ""
                    if(nodes[path[i]].floor==1):
                        floor = "first"
                    elif nodes[path[i]].floor==2:
                        floor = "second"
                    elif nodes[path[i]].floor==3:
                        floor = "third"
                    elif nodes[path[i]].floor==0:
                        floor = "ground"
                    directions_text += f' Now, use the staircase to go to the {floor} floor.'
                    continue

                elif nodes[path[i - 2]].name == 'staircase' and nodes[path[i-1]].name == 'staircase' and nodes[path[i-1]].floor != nodes[path[i - 2]].floor:
                    directions_text += " Walk straight."
                    continue

                elif(x2>x1 and y1==y2):
                    if(y3>y2 and x2==x3):
                        directions.append('Right')
                    elif(y2>y3 and x2==x3):
                        directions.append('Left')
                    elif(x3>x2 and y2==y3):
                        directions.append('Straight')
                    elif (x3 < x2 and y2 == y3):
                        directions.append('Back')
                    else:
                        directions.append('check em x2x1')

                elif (x2 < x1 and y1 == y2):
                    if (y3 > y2 and x2 == x3):
                        directions.append('Left')
                    elif (y2 > y3 and x2 == x3):
                        directions.append('Right')
                    elif (x3 > x2 and y2 == y3):
                        directions.append('Back')
                    elif (x3 < x2 and y2 == y3):
                        directions.append('Straight')
                    else:
                        directions.append('check em x1x2')

                elif (x2 == x1 and y1 < y2):
                    if (x3 > x2 and y2 == y3):
                        directions.append('Left')
                    elif (x2 > x3 and y2 == y3):
                        directions.append('Right')
                    elif (y3 < y2 and x2 == x3):
                        directions.append('Back')
                    elif (y3 > y2 and x2 == x3):
                        directions.append('Straight')
                    else:
                        directions.append('check em y2y1')

                elif (x2 == x1 and y1 > y2):
                    if (x3 > x2 and y2 == y3):
                        directions.append('Right')
                    elif (x2 > x3 and y2 == y3):
                        directions.append('Left')
                    elif (y3 < y2 and x2 == x3):
                        directions.append('Straight')
                    elif (y3 > y2 and x2 == x3):
                        directions.append('Back')
                    else:
                        directions.append('check em y1y2')

                else:
                    directions.append('Check em else')

                if(directions[-1]=='Straight'):
                    if directions[-2]!='Straight':
                        directions_text+=" Continue straight."
                else:
                    if(self.nodes[path[i-1]].name!=''):
                        directions_text+=" Now at {} turn {}.".format(self.nodes[path[i-1]].name, directions[-1])
                    else:
                        directions_text+=" Take the next "+ directions[-1] + "."
            if i==len(path)-1:
               directions_text+=" You have now arrived at "+self.nodes[dest].name+". "

        return directions, directions_text


    def dijkstra(self, src, dest):
        V = self.V
        dist = []
        minHeap = Heap()
        directions = []
        parents = [-1]*(len(self.nodes))
        path = []
        path.append(src)
        for v in range(V):
            dist.append(sys.maxsize)
            minHeap.array.append( minHeap.newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)

        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])

        minHeap.size = V

        while minHeap.isEmpty() == False:
            newHeapNode = minHeap.extractMin()

            u = newHeapNode[0]

            for pCrawl in self.graph[(u)]:
                v = pCrawl[0]
                if minHeap.isInMinHeap(v) and dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]:
                        dist[v] = pCrawl[1] + dist[u]
                        parents[v] = u
                        minHeap.decreaseKey(v, dist[v])
        path = self.getSolution(dist, parents, src, dest)
        directions, directions_text = self.getDirections(path, dest)
        return round(dist[dest], 2), path, directions, directions_text



def getPath(destination,source):
    print(source + " -->" + destination)
    src_number = map_node[source]
    if destination:
        dest_number = map_node[destination]
        floor_navigation = ""
        # if dest_number == 23 :
        #     dest_number = 1
        #     floor_navigation = " Take the stairs to reach the first floor. Turn left. Walk straight. You have now arrived at Director's Office."
        # elif dest_number == 11:
        #     dest_number = 10
        #     floor_navigation = " Take the stairs to reach the first floor. Turn left.You have now arrived at Library."
        distance, path, directions, directions_text = graph.dijkstra(src_number, dest_number)
        directions_text = directions_text + floor_navigation
        im = cv2.imread('new-ss/FINISHED/1.PNG')
        im_resized = cv2.resize(im, (610, 454), interpolation=cv2.INTER_LINEAR) ##do not change size

        img = PIL.Image.open('new-ss/FINISHED/3-MECH-0.PNG')
        #img = img.resize((610,454))
        MAX_SIZE = (24, 24) ## for thumbnail

        ## for path
        img = np.array(img)

        ## color in opencv -- BGR
        path_color = (255, 0, 0, 255)
        line_thickness = 2
        cv2.flip(im, 1)
        for i in range(len(path)-1):
            p1 = nodes[path[i]]
            p2 = nodes[path[i+1]]
            len_line = abs(p1.x-p2.x) + abs(p1.y-p2.y)

            if len_line==0:
                len_line=1

            if i==len(path)-2:
                # arrow in middle
                mid_point = ((p1.x + p2.x)//2, (p1.y + p2.y)//2)
                ## two lines
                cv2.arrowedLine(img, (p1.x, p1.y), mid_point, color=path_color, thickness=line_thickness, tipLength=13 * 2/ len_line)
                cv2.line(img, mid_point, (p2.x, p2.y), path_color, thickness=line_thickness, lineType=cv2.LINE_AA)
            else:
                cv2.arrowedLine(img, (p1.x, p1.y), (p2.x, p2.y), color=path_color, thickness=line_thickness, tipLength=13 / len_line)
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_temp = PIL.Image.fromarray(img)

        # adding source marker
        src_img = PIL.Image.open('dest.png')
        src_img.thumbnail((28,28))
        w, h = src_img.size
        paste_src_x = nodes[src_number].x - w // 2
        paste_src_y = nodes[src_number].y - h + 2
        img_temp.paste(src_img, (paste_src_x, paste_src_y))

        # adding destination marker
        dest_img = PIL.Image.open('src.png')
        dest_img.thumbnail(MAX_SIZE)
        w, h = dest_img.size
        paste_dest_x = nodes[dest_number].x - w // 2
        paste_dest_y = nodes[dest_number].y  - h + 2
        img_temp.paste(dest_img, (paste_dest_x, paste_dest_y))

        # display image
        plt.imshow(img_temp)
        plt.show()

        cv2.imwrite("display_image.jpg", img)
        print(distance)
        return directions_text
    return ""


nodes,map_node = initialize_map('nodes.json')
graph = Graph(len(nodes), nodes)
graph.addAllEdges('edges-temp.csv')

# getPath("Comps dept","Staircase main bldg/statue")
# getPath("BEE Lab","Comps dept")
# getPath("library staircase","BEE Lab")
# getPath("library staircase","Staircase main bldg/statue")

# TESTCASES FOR MAP #1
# print(getPath( "Girls hostel", "Football Field"))
# print(getPath("Girls hostel", "Boys hostel 1"))
# print(getPath("Boys hostel 2", "Cricket Ground"))

# TESTCASES FOR MAP #3
# print(getPath( "Xerox Center","Mech Gate"))
# print(getPath("Inside workshop #1", "Mech Building Entrance"))
#print(getPath( "DL002", "Mech Gate"))

# TESTCASES FOR MAP #4
print(getPath("Main Seminar Hall", "Mech Gate"))

"""
getPath("Comps dept","Staircase main bldg/statue")
sleep(2)
getPath("Library","Staircase main bldg/statue")
sleep(2)
getPath("Lab3","Canteen")
"""




