import heapq
from pandas import read_csv
from time import time

trip = input('Input: ').split(' - ')

df = read_csv('../Datasets/Flight_Data.csv')

start_time = time()

Time = 0
Distance = 1
Price = 0

heuristic_weight = 2


def calculate(distance, flyTime, price, Source, Destination):
    dijkstra = round(Time * flyTime + Distance * distance + Price * price)
    heuristic = round(
        (((Source.Latitude - Destination.Latitude) ** 2) +
         ((Source.Longitude - Destination.Longitude) ** 2) +
         ((Source.Altitude - Destination.Altitude) ** 2)) ** 0.5)
    return round(dijkstra + heuristic_weight * heuristic)


class Node:
    def __init__(self, Airport, Airport_Country, Airport_City, Latitude, Longitude, Altitude):
        # Source data
        self.Airport = Airport
        self.Country = Airport_Country
        self.City = Airport_City
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Altitude = Altitude

    def __str__(self):
        return self.City + "-" + self.Airport + ", " + self.Country


class Edge:
    def __init__(self, Source, Destination, FinalDestination, distance, flyTime, price):
        self.price = round(price, 2)
        self.flyTime = round(flyTime, 2)
        self.distance = round(distance, 2)
        self.destination = Destination
        self.source = Source
        self.weight = calculate(distance, flyTime, price, Source, FinalDestination)

    def __str__(self):
        return "From: " + str(self.source) + "\nTo: " + str(self.destination) + "\nDuration: " + str(
            self.distance) + "km\nTime: " + str(self.flyTime) + "h\nPrice: " + str(self.price) + "$"

    def __gt__(self, other):
        return self.weight > other.weight


nodes = set()
for data in df.values:
    nodes.add(data[3] + "," + data[1] + "," + data[4] + "," + str(data[5]) + "," + str(data[6]) + "," + str(data[7]))
    nodes.add(data[8] + "," + data[2] + "," + data[9] + "," + str(data[10]) + "," + str(data[11]) + "," + str(data[12]))

NodeClass = []
for i in nodes:
    data = i.split(',')
    NodeClass.append(Node(data[1], data[2], data[0], float(data[3]), float(data[4]), float(data[5])))

nodeSearch = [x.split(',')[1] for x in nodes]

SourcePath = nodeSearch.index(trip[0])
DestinationPath = nodeSearch.index(trip[1])

DestinationPathClass = NodeClass[DestinationPath]

nodes = list(nodes)
edges = []

for i in df.values:
    source = nodes.index(i[3] + "," + i[1] + "," + i[4] + "," + str(i[5]) + "," + str(i[6]) + "," + str(i[7]))
    destination = nodes.index(i[8] + "," + i[2] + "," + i[9] + "," + str(i[10]) + "," + str(i[11]) + "," + str(i[12]))
    edges.append([source, destination,
                  Edge(NodeClass[source], NodeClass[destination], DestinationPathClass, i[13], i[14], i[15])
                  ])


def ShortestPath(N, Edges, Src, Dis):
    adj = {}
    for j in range(N):
        adj[j] = []

    for s, d, edge in Edges:
        adj[s].append([d, edge.weight, edge])

    shortest = {}  # map vertex -> dict of the shortest path

    minHeap = [[0, Src, [Src], []]]

    while minHeap:
        w1, n1, way1, edge1 = heapq.heappop(minHeap)
        if n1 in shortest:
            continue
        shortest[n1] = [way1, edge1]
        if n1 == Dis:
            break

        for n2, w2, edge2 in adj[n1]:
            if n2 not in shortest:
                heapq.heappush(minHeap, [w1 + w2, n2, way1 + [n2], edge1 + [edge2]])

    for k in range(N):
        if k not in shortest:
            shortest[k] = -1

    return shortest


answer = ShortestPath(len(nodes), edges, SourcePath, DestinationPath)[nodeSearch.index(trip[1])][1]

execution_time = round(time() - start_time, 2)

output = "A star Algorithms\n"
output += "Execution Time: " + str(execution_time) + "s\n"
output += '----------------------------\n'

Duration = 0
FlyTime = 0
Price = 0
index = 1
for i in answer:
    output += 'Flight #' + str(index) + ":\n"
    index += 1
    Duration += round(i.distance)
    Time += round(i.flyTime)
    Price += round(i.price)
    output += str(i) + "\n----------------------------\n"

output += "total Price: " + str(Price) + "$\n"
output += "total Duration: " + str(Duration) + "KM\n"
output += "total Fly Time : " + str(Time) + "H\n"

f = open("../Outputs/The_Phoenix-UIAI4021-PR1-Q1(A-star).txt", "w")
f.write(output)
f.close()

print('Done')
