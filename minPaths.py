from graph import Graph
from collections import defaultdict, deque
import sys
class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])

    # def dijkstra(self, src):
    #     #unvisited and visited nodes
    #     unvisited = []
    #     visited = []
    #     values = [0]*self.V
    #     for i in range(self.V):
    #         unvisited.append(i)
    #     visited.append(src)
    #     values[src] = 0

    def minDistance(self, dist, temp):

        # Initialize minimum distance for next node
        min = sys.maxsize
        min_index = 0
        # Search not nearest vertex not in the
        # shortest path tree
        for u in range(self.V):
            if dist[u] < min and temp[u] == False:
                min = dist[u]
                min_index = u

        return min_index

    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        temp = [False] * self.V
        steps = [[] for _ in range(self.V)]
        steps[src] = [src]

        for _ in range(self.V):
            x = self.minDistance(dist, temp)

            temp[x] = True

            for y in range(self.V):
                if self.graph[x][y] > 0 and temp[y] == False and \
                        dist[y] > dist[x] + self.graph[x][y]:
                    dist[y] = dist[x] + self.graph[x][y]
                    steps[y] = steps[x] + [y]
        for i in range(self.V):
            if(dist[i] == sys.maxsize):
                dist[i] = "no connection"
            print(i, "\t", dist[i], steps[i])

    def read_file(path):
        data = []
        with open(path, 'r') as file:
            # Read the entire file content
            content = file.read().splitlines()
        N = int(content[0].strip())
        for i in range(1,6):
            x = list(map(int, content[i].strip().split()))
            data.append(x)
        return N, data



if __name__ == "__main__":
    name="MinPaths_data5.txt"
    N, data = Graph.read_file(name)
    g = Graph(N)
    g.graph = data
    g.dijkstra(4)







#policzyć wszystkie drogi
#wyznaczyć nakrótsze drogi
#cel: