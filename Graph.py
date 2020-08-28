from collections import defaultdict
import sys
from Heap import Heap
import csv
import json
from Node import Node
from math import sqrt


def initialize_map(filename):
    f = open(filename)
    data = json.load(f)
    nodes = []
    for _, node in data.items():
        temp_node = Node(
            number=node["number"],
            name=node["name"],
            x=int(node["x"]),
            y=int(node["y"]),
            node_type=node["type"],
            floor=int(node["floor"]),
            building=node["building"]
        )
        nodes.append(temp_node)
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

    def dijkstra(self, src, dest):
        V = self.V

        dist = []
        minHeap = Heap()
        directions = [] ## for directions - revathi
        path = [] ## for actual path - revathi
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
            path.append(u)
            if u==dest:
                return round(dist[u], 2), path

            for pCrawl in self.graph[(u)]:
                v = pCrawl[0]
                if minHeap.isInMinHeap(v) and dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]:
                        dist[v] = pCrawl[1] + dist[u]
                        minHeap.decreaseKey(v, dist[v])
        print("Path: ", path)
        print(self.graph[u])
        return dist[dest]

    #TODO: add directions switch case

## driver code to test
if __name__=='__main__':
    nodes = initialize_map('nodes.json')
    graph = Graph(34, nodes)
    graph.addAllEdges('edges.csv')
    distance, path = graph.dijkstra(1, 7)
    print("Distance: ", distance)
    print("Path: ", path)
    op_path = "" ## revathi: building op path as string -- change to list later 
    for node in path:
        node_name = nodes[node].name
        if(node_name==""):
            continue
        else:
            op_path = op_path + str(node_name) + " --> "
    print("Output path: ", op_path)
