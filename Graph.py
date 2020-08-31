from collections import defaultdict
import sys
from Heap import Heap
import csv
import json
import re
from Node import Node
from math import sqrt
from time import sleep

"""
{0: Main Gate , 1: , 2: Main Building Entrace, 3: , 4: Main Building Staircase, 5: Director's Office,
6: Lab 3, 7: Dep1 , 8: Dep2 , 9: , 10: Computer Department, 11: Study Space , 12: , 13: AL004 ,
14: , 15: Stage , 16: , 17: Audi Entrance, 18: Stage Washroom, 19: Canteen Quad Entrance,
20: Quad , 21: Quad Steps, 22: , 23: , 24: , 25: , 26: CCF1, 27: Library,
28: Library Staircase, 29: COE, 30: , 31: Electrical Dept/Staircase, 32: Statue, 33: Quad Entrance}

"""


def initialize_map(filename):
    f = open(filename)
    data = json.load(f)
    nodes = {}
    for key, node in data.items():
        temp_node = Node(
            number=node["number"], ## dont change this to -1
            name=node["name"],
            x=int(node["x"]),
            y=int(node["y"]),
            node_type=node["type"],
            floor=int(node["floor"]),
            building=node["building"]
        )
        nodes[int(key)-1] = temp_node
    return nodes


class Graph():

    def __init__(self, V, nodes):
        self.V = V
        self.graph = defaultdict(list)
        self.nodes = nodes

    def calculateDistance(self, src, dest):
        return sqrt(pow(nodes[src].x - nodes[dest].x, 2)+pow(nodes[src].y-nodes[dest].y, 2))

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
                self.addEdge(int(row['Node '])-1, int(row['Adjacents'])-1)

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

    def getDirections(self, path):
        directions = []
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
                    directions.append('Up')
                elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y < self.nodes[prev].y:
                    directions.append('Down')
            else:
                x_curr, y_curr = self.nodes[path[i]].x, self.nodes[path[i]].y
                x_prev, y_prev = self.nodes[path[i-1]].x, self.nodes[path[i-1]].y
                x_prev_prev, y_prev_prev = self.nodes[path[i-2]].x, self.nodes[path[i-2]].y
                # print("current: ", f'{x_curr}, {y_curr}')
                # print("Prev: ", f'{x_prev}, {y_prev}')
                # print("Prev prev: ", f'{x_prev_prev}, {y_prev_prev}')
                if y_prev==y_curr==y_prev_prev and ((x_curr > x_prev and x_prev > x_prev_prev) or (x_curr < x_prev and x_prev < x_prev_prev)):
                    directions.append('Straight')
                elif x_prev==x_curr==x_prev_prev and ((y_curr > y_prev and y_prev > y_prev_prev) or (y_curr < y_prev and y_prev < y_prev_prev)):
                    directions.append('Straight')
                elif abs(x_curr-x_prev)<=5 and abs(x_prev-x_prev_prev)<=5 and (abs(y_prev_prev-y_prev)<=5 and y_prev > y_curr):
                    directions.append("Right")
                elif abs(x_curr-x_prev)<=5 and x_prev > x_prev_prev and (abs(y_prev_prev-y_prev)<=5 and y_prev < y_curr):
                    directions.append("Left")
                elif abs(x_curr-x_prev)<=5 and x_prev < x_prev_prev and (abs(y_prev_prev-y_prev)<=5 and y_prev > y_curr):
                    directions.append("Left")
                elif abs(x_curr-x_prev)<=5 and x_prev < x_prev_prev and (abs(y_prev_prev-y_prev)<=5 and y_prev < y_curr):
                    directions.append("Right")
                elif x_curr > x_prev and abs(x_prev-x_prev_prev)<=5 and (abs(y_prev-y_curr)<=5 and y_prev > y_curr):
                    directions.append("Left")
                elif x_curr < x_prev and abs(x_prev-x_prev_prev)<=5 and (abs(y_prev-y_curr) and y_prev > y_curr):
                    directions.append("Right")

        return directions


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
        path = self.getSolution(dist, parents, source, dest)
        directions = self.getDirections(path)
        return round(dist[dest], 2), path, directions

    #TODO: add directions switch case



## driver code to test
if __name__=='__main__':

    source = 0
    dest = 18 #20, 19, 27, 30

    #TODO: code to redirect to nearest staircase - pseudo code written
    # if nodes[dest].floor==1:
    #     for node in adj_list of dest
    #         if re.find('staircase') in nodes[dest].name:
    #             dest = that node

    nodes = initialize_map('nodes.json')
    # print(nodes)

    graph = Graph(34, nodes)
    graph.addAllEdges('edges.csv')
    distance, path, directions = graph.dijkstra(source, dest)

    print("Source: ", nodes[source].name)
    print("Destination: ", nodes[dest].name)
    # print("Directions: ", directions)
    print("Path: ", path)
    for i in range(len(path)):
        if nodes[path[i]].name=="":
            print(" turning/junction ", end='')
        if i!=len(path)-1:
            print(nodes[path[i]].name, end=" -- > ")
        else:
            print(nodes[path[i]].name)
    # for i in range(len(path)):
    #     print(f"x: {nodes[path[i]].x}, y: {nodes[path[i]].y}")
