from collections import defaultdict

class Graph:
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)

    def read_file(path):
        data = []
        with open(path, 'r') as file:
            # Read the entire file content
            content = file.read().splitlines()
        N = int(content[0].strip())
        for i in range(1,N+1):
            x = list(map(int, content[i].strip().split()))
            data.append(x)
        return N, data
    
    def BFS(self, s, t, parent):
        """
        Performs Breadth-First Search to find an augmenting path.

        Args:
            s: Source node.
            t: Sink node.
            parent: Array to store the parent node for each node in the path.

        Returns:
            True if an augmenting path is found, False otherwise.
        """
        visited = [False] * self.ROW
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    def FordFulkerson(self, source, sink):
        """
        Implements the Ford-Fulkerson algorithm to find the maximum flow.

        Args:
            source: Source node.
            sink: Sink node.

        Returns:
            The maximum flow value.
        """
        parent = [-1] * self.ROW
        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

# Example graph
N, graph = Graph.read_file("MaxFlows_data5.txt")

print(graph)
g = Graph(graph)
source = 0
sink = N-1

max_flow = g.FordFulkerson(source, sink)

print("Maximum flow:", max_flow)