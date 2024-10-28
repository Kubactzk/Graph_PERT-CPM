from collections import defaultdict, deque
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def addEdge(self,u,v):
        self.graph[u].append(v)

    def calculateInOut(self):
        indegrees = [0] * self.V
        outdegreees = [0] * self.V

        for i in self.graph:
            for j in self.graph[i]:
                indegrees[j-1] += 1
            outdegreees[i-1] = len(self.graph[i])

        return indegrees,outdegreees

    def topologicalSort(self):
        indegrees, outdegreees = self.calculateInOut()
        totalInOut=[]
        for i in range(self.V):
            totalInOut.append((indegrees[i],outdegreees[i]))

        queue = deque([i for i in range(self.V) if indegrees[i] == 0])
        totalInOut = []
        topological_order = []
        while queue:
            vertex = queue.popleft()
            topological_order.append(vertex + 1)  # Store in topological order, adjusting for 1-based index

            # For each adjacent node, decrease the in-degree
            for neighbor in self.graph[vertex + 1]:
                indegrees[neighbor - 1] -= 1
                # If in-degree becomes zero, add to queue
                if indegrees[neighbor - 1] == 0:
                    queue.append(neighbor - 1)
        return topological_order

    def caluculate_Bellman(self, durations):
        indegrees, outdegreees = self.calculateInOut()

        ES = [0] * self.V
        EF = [0] * self.V
        LS = [0] * self.V
        LF = [0] * self.V
        finalData = defaultdict(list)
        criticalPath = []
        processTime = 0
        # One Bellman-Ford
        for _ in range(self.V):  # Repeat relaxation V times
            for j in range(1, self.V + 1):  # 1-based task numbering
                for k in self.graph[j]:
                    # Adjust for 0-based index in ES, EF, and durations
                    ES[k - 1] = max(ES[k - 1], ES[j - 1] + durations[j - 1])
        # Calculate EF based on ES + duration
        EF = [ES[i] + durations[i] for i in range(self.V)]
        processTime = max(EF)

        for i in reversed(self.topologicalSort()):
            i_idx = i - 1
            if not self.graph[i]:
                LF[i_idx] = processTime
                LS[i_idx] = LF[i_idx] - durations[i_idx]
            else:
                temp=[]
                for j in self.graph[i]:
                    temp.append(LS[j - 1])
                    LF[i_idx] = min(temp)
                LS[i_idx] = LF[i_idx] - durations[i_idx]

        for i in range(self.V):
            finalData[i].append((ES[i],EF[i],LS[i],LF[i]))
            tf1 = LS[i] - ES[i]
            tf2 = LF[i] - EF[i]
            if(tf1 + tf2 == 0):
                criticalPath.append((i+1,ES[i],EF[i]))

        return finalData, processTime, criticalPath


    def readData(path):
        with open(path, 'r') as file:
            # Read the entire file content
            content = file.read().splitlines()
        N, M = map(int, content[0].split())
        durations = list(map(int, content[1].strip().split()))
        dependencies = []
        dependency_data = list(map(int, content[2].strip().split()))
        for i in range(0, len(dependency_data), 2):
            a, b = dependency_data[i], dependency_data[i + 1]
            dependencies.append((a, b))

        return N, M, durations, dependencies





if __name__ == "__main__":
    name = "data10.txt"
    n,m, durations, dependencies = Graph.readData(name)
    g = Graph(n)
    for i in dependencies:
        g.addEdge(i[0],i[1])

    x = g.topologicalSort()
    finalData, processTime, criticalPath = g.caluculate_Bellman(durations)
    print("Graph:", g.graph)
    print("Topological Sort:", x)
    print("Process number: ES, EF, LS, LF\t")
    for i in range(n):
        print(f"{i+1}: {finalData[i]}")
    print("Process time:", processTime)
    counter = 0
    for i in criticalPath:
        counter+=1
        print(f"Critical path no.{counter}: {i}")

