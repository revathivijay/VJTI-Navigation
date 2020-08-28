from collections import defaultdict
import sys
from Heap import Heap
from Node import Node

class Graph():

    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)

    def addEdge(self, src, dest, weight):
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

    def dijkstra(self, src):
        V = self.V
        dist = []
        minHeap = Heap()

        for v in range(V):
            dist.append(sys.maxsize) ## python3
            minHeap.array.append( minHeap.newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)

        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])

        minHeap.size = V;

        while minHeap.isEmpty() == False:
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]
            for pCrawl in self.graph[u]:
                v = pCrawl[0]
                if minHeap.isInMinHeap(v) and dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]:
                        dist[v] = pCrawl[1] + dist[u]
                        minHeap.decreaseKey(v, dist[v])

        # printArr(dist,V)

## driver code to test
if __name__=='__main__':
    # graph = Graph(9)
    # graph.addEdge(0, 1, 4)
    # graph.dijkstra(0)
    print("In dijkstra")

    ## add code for adding edges 
