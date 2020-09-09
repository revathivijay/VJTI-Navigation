from collections import defaultdict
import sys
from Heap import Heap
import csv
import json
import re
from Node import Node
from math import sqrt
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

"""
{0: Main Gate , 1: , 2: Main Building Entrace, 3: , 4: Main Building Staircase, 5: Director's Office,
6: Lab 3, 7: Dep1 , 8: Dep2 , 9: , 10: Computer Department, 11: Study Space , 12: , 13: AL004 ,
14: , 15: Stage , 16: , 17: Audi Entrance, 18: Stage Washroom, 19: Canteen Quad Entrance,
20: Quad , 21: Quad Steps, 22: , 23: , 24: , 25: , 26: CCF1, 27: Library,
28: Library Staircase, 29: COE, 30: , 31: Electrical Dept/Staircase, 32: Statue, 33: Quad Entrance}

"""

## for viusalizing
pixel_mapping = {
    0:(340,444),
    1:(340,380),
    2:(397,380),
    3:(466,380),
    4:(534,380),
    5:(534,287),
    6:(490,287),
    7:(490,264),
    8:(421,287),
    9:(421,221),
    10:(421,127),
    11:(466,127),
    12:(330,127),
    13:(263,127),
    14:(263,219),
    15:(350,219),
    16:(250,283),
    17:(263,286),
    18:(263,333),
    19:(263,380),
    20:(215,380),
    21:(126,444),
    22:(54,444),
    23:(101,390)
}


def initialize_map(filename):
    f = open(filename)
    data = json.load(f)
    nodes = {}
    for key, node in data.items():
        temp_node = Node(
            number=node["Node number"], ## dont change this to -1
            name=node["Node Name"],
            x=int(node["x_pos"]),
            y=int(node["y_pos"]),
            node_type=node["Type "],
            floor=int(node["Floor"]),
            building=node["Building"]
        )
        nodes[int(key)-1] = temp_node
    return nodes


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
                self.addEdge(int(row['Nodes']), int(row['Adjacents']))

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
                if(x2>x1 and y1==y2):
                    if(y3>y2 and x2==x3):
                        directions.append('Left')
                    elif(y2>y3 and x2==x3):
                        directions.append('Right')
                    elif(x3>x2 and y2==y3):
                        directions.append('Straight')
                    elif (x3 < x2 and y2 == y3):
                        directions.append('Back')
                    else:
                        directions.append('check em x2x1')

                elif (x2 < x1 and y1 == y2):
                    if (y3 > y2 and x2 == x3):
                        directions.append('Right')
                    elif (y2 > y3 and x2 == x3):
                        directions.append('Left')
                    elif (x3 > x2 and y2 == y3):
                        directions.append('Back')
                    elif (x3 < x2 and y2 == y3):
                        directions.append('Straight')
                    else:
                        directions.append('check em x1x2')

                elif (x2 == x1 and y1 < y2):
                    if (x3 > x2 and y2 == y3):
                        directions.append('Right')
                    elif (x2 > x3 and y2 == y3):
                        directions.append('Left')
                    elif (y3 < y2 and x2 == x3):
                        directions.append('Back')
                    elif (y3 > y2 and x2 == x3):
                        directions.append('Straight')
                    else:
                        directions.append('check em y2y1')

                elif (x2 == x1 and y1 > y2):
                    if (x3 > x2 and y2 == y3):
                        directions.append('Left')
                    elif (x2 > x3 and y2 == y3):
                        directions.append('Right')
                    elif (y3 < y2 and x2 == x3):
                        directions.append('Straight')
                    elif (y3 > y2 and x2 == x3):
                        directions.append('Back')
                    else:
                        directions.append('check em y1y2')

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
        directions = [] ## for directions - revathi
        parents = [-1]*(len(self.nodes)) ## for path - revathi
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

        #TODO: modify to show proper route -- done revathi
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

    #TODO: add directions switch case



## driver code to test
def getPath():

    source = 1
    dest = 12 #20, 19, 27, 30

    #TODO: code to redirect to nearest staircase - pseudo code written
    # if nodes[dest].floor==1:
    #     for node in adj_list of dest
    #         if re.find('staircase') in nodes[dest].name:
    #             dest = that node

    nodes = initialize_map('nodes.json')
    # print(nodes)

    graph = Graph(25, nodes)
    graph.addAllEdges('edges.csv')
    distance, path, directions, directions_text = graph.dijkstra(source, dest)

    print("Source: ", nodes[source].name)
    print("Destination: ", nodes[dest].name)
    print("Directions: ", directions)
    print("Path: ", path)
    for i in range(len(path)):
        if nodes[path[i]].name=="":
            print(" turning/junction ", end='')
        if i!=len(path)-1:
            print(nodes[path[i]].name, end=" -- > ")
        else:
            print(nodes[path[i]].name)


    print("The directions are: " + directions_text)

    ## visualizing part -- revathi
    im = cv2.imread('MAP.jpeg')
    im_resized = cv2.resize(im, (610, 454), interpolation=cv2.INTER_LINEAR) ##do not change size
    line_thickness = 5
    color = (0, 0, 0)
    for i in range(len(path)-1):
        p1 = pixel_mapping[path[i]]
        p2 = pixel_mapping[path[i+1]]
        cv2.line(im_resized, p1, p2, color=color, thickness=line_thickness)
    plt.imshow(cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGB))
    plt.show()
    return path

    # for i in range(len(path)):
    #     print(f"x: {nodes[path[i]].x}, y: {nodes[path[i]].y}")
if __name__ == '__main__':
    getPath()
