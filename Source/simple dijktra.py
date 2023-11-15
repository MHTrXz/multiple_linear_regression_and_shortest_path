# https://youtu.be/XEb7_z5dG3c?si=hE5rwWGypR5ytY7_

import heapq

n = 5
edges = [[0, 1, 10], [0, 2, 3], [1, 3, 2], [2, 1, 4], [2, 3, 8], [2, 4, 2], [3, 4, 5]]
src = 0

adj = {}
for i in range(n):
    adj[i] = []

for s, d, weight in edges:
    adj[s].append([d, weight])

shortest = {}  # map vertex -> dict of the shortest path

minHeap = [[0, src, [0]]]

while minHeap:
    w1, n1, way1 = heapq.heappop(minHeap)
    if n1 in shortest:
        continue
    shortest[n1] = way1

    for n2, w2 in adj[n1]:
        if n2 not in shortest:
            heapq.heappush(minHeap, [w1 + w2, n2, way1 + [n2]])

for i in range(n):
    if i not in shortest:
        shortest[i] = -1

print(shortest)
