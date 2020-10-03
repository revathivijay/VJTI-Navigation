from collections import defaultdict
import sys
from Heap import Heap
import csv
import json
import re
from Node import Node
from math import sqrt
from time import sleep
from google_drive_util import create_file
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from googletrans import Translator
translator = Translator()
import numpy as np
import PIL
import requests
from PIL import Image
import glob
from save_image import save_image
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

def initialize_map(filename):
    f = open(filename)
    data = json.load(f)
    nodes = {}
    map_node = {}
    for key, node in data.items():
        temp_node = Node(
            number=int(node["Node number"]), ## dont change this to -1
            name=node["Node Name"],
            x=int(node["x_pos"]),
            y=int(node["y_pos"]),
            node_type=node["Type "],
            floor=int(node["Floor"]),
            building=node["Building"],
            map = int(node["Map Number"])
        )
        nodes[int(key)-1] = temp_node
        map_node[node["Node Name"]] = int(node["Node number"])-1
    return nodes,map_node

def get_image_mapping(filename):
    f = open(filename)
    data = json.load(f)
    images = {}
    for key, value in data.items():
        images[key] = value
    return images


class Graph():

    def __init__(self, V, nodes):
        self.V = V
        self.graph = defaultdict(list)
        self.nodes = nodes

    def calculateDistance(self, src, dest):
        return sqrt(pow(self.nodes[src].x - self.nodes[dest].x + abs(self.nodes[src].map - self.nodes[dest].map)*639, 2)+pow(self.nodes[src].y-self.nodes[dest].y + abs(self.nodes[src].map - self.nodes[dest].map)*540, 2))

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
                if path[0]== 16: #Mech Gate
                    curr = path[i]
                    prev = path[i - 1]
                    if self.nodes[curr].x > self.nodes[prev].x and self.nodes[curr].y == self.nodes[prev].y:
                        directions.append('Right')
                    elif self.nodes[curr].x < self.nodes[prev].x and self.nodes[curr].y == self.nodes[prev].y:
                        directions.append('Left')
                    elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y > self.nodes[prev].y:
                        directions.append('Back')
                    elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y < self.nodes[prev].y:
                        directions.append('Straight')
                    else:
                        directions.append("check em")
                elif path[0]==5:  # Girls Hostel
                    curr = path[i]
                    prev = path[i - 1]
                    if self.nodes[curr].x > self.nodes[prev].x and self.nodes[curr].y == self.nodes[prev].y:
                        directions.append('Straight')
                    elif self.nodes[curr].x < self.nodes[prev].x and self.nodes[curr].y == self.nodes[prev].y:
                        directions.append('Back')
                    elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y > self.nodes[prev].y:
                        directions.append('Right')
                    elif self.nodes[curr].x == self.nodes[prev].x and self.nodes[curr].y < self.nodes[prev].y:
                        directions.append('Left')
                    else:
                        directions.append("check em")

                else: #Main Gate and default case (shouldnt be called for default!)
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
                    elif path[0] in (33, 41) or path[0] in (48, 52):
                        directions.append("Straight")
                    else:
                        directions.append("Check em")



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

                elif self.nodes[path[i-1]].name=='staircase' and self.nodes[path[i]].name == 'staircase' and self.nodes[path[i]].floor != self.nodes[path[i-1]].floor:
                    floor = ""
                    if(self.nodes[path[i]].floor==1):
                        floor = "first"
                    elif self.nodes[path[i]].floor==2:
                        floor = "second"
                    elif self.nodes[path[i]].floor==3:
                        floor = "third"
                    elif self.nodes[path[i]].floor==0:
                        floor = "ground"
                    directions_text += f' Now, use the staircase to go to the {floor} floor.'

                    if i == len(path) - 1:
                        if ('washroom' in self.nodes[dest].name):
                            directions_text += " You have reached the washroom."
                        else:
                            directions_text += f"You have arrived at {nodes[path[i]].name}"
                    continue

                elif self.nodes[path[i - 2]].name == 'staircase' and self.nodes[path[i-1]].name == 'staircase' and self.nodes[path[i-1]].floor != self.nodes[path[i - 2]].floor:
                    directions_text += " Walk straight."
                    if i == len(path) - 1:
                        if ('washroom' in self.nodes[dest].name):
                            directions_text += " You have reached the washroom."
                        else:
                            directions_text += f"You have arrived at {self.nodes[path[i]].name}"
                    continue

                # Map Connectors
                elif path[i-2]==0 or path[i-1] == 0 or path[i-2]==90 or path[i-1]==90 or path[i-2]==92 or path[i-1]==92 or path[i-2]==13 or path[i-1]==13:
                    directions.append("Straight")

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

                if i == len(path) - 1:
                    if ('washroom' in self.nodes[dest].name):
                        directions_text += " You have reached the washroom."
                    else:
                        directions_text += f"You have arrived at {self.nodes[path[i]].name}"


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
            minHeap.array.append(minHeap.newMinHeapNode(v, dist[v]))
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


# This function is created to find washroom closest washroom
def findDestination(src, dest, gender):
    #Repromt to ask girls/boys washroom
    all_dests = []
    dist = []
    if(dest=="washroom"):
        for i in range(len(nodes)):
            if "washroom" in nodes[i].name and gender in nodes[i].name:
                all_dests.append(nodes[i])
                dist.append(graph.calculateDistance(map_node[src], nodes[i].number))
    else:
        for i in range(len(nodes)):
            if dest in nodes[i].name :
                all_dests.append(nodes[i])
                dist.append(graph.calculateDistance(map_node[src], nodes[i].number))

    dest = all_dests[dist.index(min(dist))]
    return dest.number



def getPath(destination,source, gender="null"):
    print(source + " -->" + str(destination))
    src_number = map_node[source]
    dest_number = findDestination(source, destination, gender)
    if dest_number:
        distance, path, directions, directions_text = graph.dijkstra(src_number, dest_number)

        MAX_SIZE = (24, 24) ## for thumbnail
        path_color = (0, 0, 0, 255) ##black path
        line_thickness = 2

        img = PIL.Image.open(f'resized-new/{nodes[src_number].map}-{nodes[src_number].floor}.jpg')
        img = np.array(img)
        img_temp = PIL.Image.fromarray(img)
        curr_map = nodes[src_number].map
        curr_floor = nodes[src_number].floor
        counter = 0
        src_map = nodes[src_number].map
        dest_map = nodes[dest_number].map
        src_floor = nodes[src_number].floor
        dest_floor = nodes[dest_number].floor
        print("PATH: ", path)
        for i in range(len(path)-1):
            p1 = nodes[path[i]]
            p2 = nodes[path[i+1]]

            if i==0 and (src_map!=dest_map or src_floor!=dest_floor):
                src_img = PIL.Image.open('dest.png')
                src_img.thumbnail((28, 28))
                w, h = src_img.size
                paste_src_x = nodes[src_number].x - w // 2
                paste_src_y = nodes[src_number].y - h + 2
                img_temp.paste(src_img, (paste_src_x, paste_src_y))
                img = np.array(img_temp)

            if (curr_map!=p1.map or curr_floor!=p1.floor):
                img = np.array(img_temp)
                # plt.imshow(img)
                # plt.show()
                # cv2.imwrite(f"all-dest/{src_number}-{dest_number}-{counter}.jpg", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                cv2.imwrite(f"temp-output/{src_number}-{dest_number}-{curr_map}-{curr_floor}-{counter}.jpg", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                counter+=1
                curr_map = p1.map
                curr_floor = p1.floor
                img = PIL.Image.open(f'resized-new/{curr_map}-{curr_floor}.jpg')
                img = np.array(img)
                img_temp = PIL.Image.fromarray(img)

            len_line = abs(p1.x-p2.x) + abs(p1.y-p2.y)

            if len_line==0:
                len_line=1

            if i==len(path)-2:
                # arrow in middle
                mid_point = ((p1.x + p2.x)//2, (p1.y + p2.y)//2)
                ## two lines
                cv2.arrowedLine(img, (p1.x, p1.y), mid_point, color=path_color, thickness=line_thickness, tipLength=13 * 2/ len_line)
                cv2.line(img, mid_point, (p2.x, p2.y), path_color, thickness=line_thickness, lineType=cv2.LINE_AA)
                if src_map!=dest_map or src_floor!=dest_floor:
                    img_temp = PIL.Image.fromarray(img)
                    dest_img = PIL.Image.open('src.png')
                    dest_img.thumbnail(MAX_SIZE)
                    w, h = dest_img.size
                    paste_dest_x = nodes[dest_number].x - w // 2
                    paste_dest_y = nodes[dest_number].y - h + 2
                    img_temp.paste(dest_img, (paste_dest_x, paste_dest_y))
                    img = np.array(img_temp)
            elif(p2.map==p1.map and p2.floor==p1.floor):
                cv2.arrowedLine(img, (p1.x, p1.y), (p2.x, p2.y), color=path_color, thickness=line_thickness, tipLength=13 / len_line)
                img_temp = PIL.Image.fromarray(img)

        ## if both dest and source are on same map
        if src_map==dest_map and src_floor==dest_floor:
            img_temp = PIL.Image.fromarray(img)

            ## adding source marker
            src_img = PIL.Image.open('dest.png')
            src_img.thumbnail((28, 28))
            w, h = src_img.size
            paste_src_x = nodes[src_number].x - w // 2
            paste_src_y = nodes[src_number].y - h + 2
            img_temp.paste(src_img, (paste_src_x, paste_src_y))

            # adding destination marker
            dest_img = PIL.Image.open('src.png')
            dest_img.thumbnail(MAX_SIZE)
            w, h = dest_img.size
            paste_dest_x = nodes[dest_number].x - w // 2
            paste_dest_y = nodes[dest_number].y - h + 2
            img_temp.paste(dest_img, (paste_dest_x, paste_dest_y))

        print(src_number, " ", dest_number, " ", counter)

        # display image
        img = np.array(img_temp)

        # plt.imshow(img)
        # plt.show()
        # cv2.imwrite(f"all-dest/{src_number}-{dest_number}-{counter}.jpg", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        cv2.imwrite(f"temp-output/{src_number}-{dest_number}-{curr_map}-{curr_floor}-{counter}.jpg",
                    cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        print(distance)

        # for saving final image
        count = 0
        output_images = []

        ## TODO: change to whatever path we're reading from in actual appln
        for name in glob.glob(f'C:\\Users\\rohan\\Desktop\\Revathi\\VJTI-Navigation-master\\VJTI-Navigation-master\\temp-output\\{src_number}-{dest_number}-*'):
            print(name)
            count +=1
            output_images.append(name)

        ## for alignment of maps 2-0 2-1 special cases
        case2 = True
        if src_map==2 and dest_map==2 and src_floor==1 and dest_floor==0:
            case2 = False
        save_image(output_images, count, src_number, dest_number, case2)
        return directions_text
    return ""



""" Library Path Test
getPath("Comps dept","Staircase main bldg/statue")
getPath("BEE Lab","Comps dept")
getPath("library staircase","BEE Lab")
getPath("library staircase","Staircase main bldg/statue")
"""

"""
Hindi Skill Code
text = getPath("Library","Staircase main bldg/statue")
print(text)
text = text.replace("Take the next Left","Take the next left turn")
text = text.replace("Take the next Right","Take the next right turn")
print(text)
result = translator.translate(text,src='en', dest='hi')
print(result.text)
"""

def uploadImage(src_number,dest_number):

    if dest_number:
        distance, path, directions, directions_text = graph.dijkstra(src_number, dest_number)
        im = cv2.imread('MAP.jpeg')
        im_resized = cv2.resize(im, (610, 454), interpolation=cv2.INTER_LINEAR) ##do not change size
        line_thickness = 3

        ## color in opencv -- BGR
        path_color = (0, 0, 0)
        src_color = (13,64,0)
        dest_color = (255,0,0)
        circle_thickness = 12

        ## legends
        cv2.circle(im_resized, (25, 25), 10, src_color, thickness=circle_thickness)
        cv2.putText(im_resized, f'{nodes[src_number].name} (you are here)', (50,27), cv2.FONT_HERSHEY_SIMPLEX , 0.7, path_color, 2, cv2.LINE_AA)

        cv2.circle(im_resized, (25,67), 10, dest_color, thickness=circle_thickness)
        cv2.putText(im_resized, f'{nodes[dest_number].name} (destination)', (50,71), cv2.FONT_HERSHEY_SIMPLEX , 0.7, path_color, 2, cv2.LINE_AA)

        ## source and dest markers
        cv2.circle(im_resized, (pixel_mapping[src_number][0], pixel_mapping[src_number][1]), 10, src_color, thickness=circle_thickness)
        cv2.circle(im_resized, (pixel_mapping[dest_number][0], pixel_mapping[dest_number][1]), 10, dest_color, thickness=circle_thickness)

        for i in range(len(path)-1):
            p1 = pixel_mapping[path[i]]
            p2 = pixel_mapping[path[i+1]]
            len_line = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
            if len_line==0:
                len_line=1
            cv2.arrowedLine(im_resized, p1, p2, color=path_color, thickness=line_thickness, tipLength=13/len_line)
        #plt.imshow(cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGB))
        #plt.show()
        cv2.imwrite("display_image.jpg", im_resized)
        filename_on_drive =  str(src_number) + "_" + str(dest_number) + ".jpg"
        id = create_file(filename="display_image.jpg",filename_on_drive=filename_on_drive)
        return id,filename_on_drive

# img = Image.open('new-ss/FINISHED/2-0.PNG')
# plt.imshow(img)
# for i in range(len(nodes)):
#     for j in graph.graph[i]:
#         v = j[0]
#         if(nodes[i].map==2 and nodes[v].map ==2 and nodes[i].floor==0 and nodes[v].floor==0):
#             plt.plot(nodes[i].x, nodes[i].y, 'o')
#             plt.plot(nodes[v].x, nodes[v].y, 'o')
#             plt.plot([nodes[i].x, nodes[v].x], [nodes[i].y, nodes[v].y])
#             plt.text(nodes[i].x + 10, nodes[i].y, i+ 1)

# plt.show()

nodes, map_node = initialize_map('nodes.json')
graph = Graph(len(nodes), nodes)
graph.addAllEdges('edges-rev.csv')


# img = Image.open('resized-new/2-1.jpg')
# plt.imshow(img)
# for i in range(len(nodes)):
#     for j in graph.graph[i]:
#         v = j[0]
#         if(nodes[i].map==2 and nodes[v].map == 2  and nodes[i].floor==1 and nodes[v].floor==1):
#             plt.plot(nodes[i].x, nodes[i].y, 'o')
#             plt.plot(nodes[v].x, nodes[v].y, 'o')
#             plt.plot([nodes[i].x, nodes[v].x], [nodes[i].y, nodes[v].y])
#             plt.text(nodes[i].x + 10, nodes[i].y, i+ 1)
# plt.show()

# TESTCASES FOR MAP #2
# print(getPath("BCT Lab","statue"))
# print(getPath("Xerox Center","statue"))
# print(getPath("girls washroom","director office"))

# # TESTCASES FOR MAP #1
# print(getPath( "Girls hostel", "Football Field"))
# print(getPath("Girls hostel", "Boys hostel 1"))

# TESTCASES FOR MAP #3
# print(getPath( "Xerox Center","Mech Gate"))
# print(getPath("Inside workshop #1", "Mech Building Entrance"))
# print(getPath( "director office", "Main Seminar Hall"))
# print(getPath( "Quad", "Main Seminar Hall"))

# TESTCASES FOR MAP #4
# print(getPath("Main Seminar Hall", "Mech Gate"))

# TESTCASES FOR WASHROOM
# print(getPath("Girls hostel", "canteen"))

# # TESTCASES FOR MULTIPLE MAPS
# print(getPath("Cricket Ground", "main gate"))
# print(getPath("Main Seminar Hall", "Cricket Ground"))
import time
## generating all output maps
with open('locations.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Pass reader object to list() to get a list of lists
    loc = list(csv_reader)
    for i in range(len(loc)):
        loc[i]= "".join(loc[i])
    print(loc)
    st = time.time()
    for i in range(len(loc)):
        for j in range(len(loc)):
            if(map_node[loc[i]] not in range(34, 41)):
                print(getPath(loc[i], loc[j]))
            if (map_node[loc[j]] not in range(34, 41)):
                print(getPath(loc[j], loc[i]))

    end = time.time()
    print("Time taken: ", str(end-st), "s")



