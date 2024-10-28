from graph import Graph
import random
import matplotlib.pyplot as plt


def readData_pertTriangle(path):
    with open(path, 'r') as file:
        # Read the entire file content
        content = file.read().splitlines()
    N, M = map(int, content[0].split())
    durations = list(map(int, content[1].strip().split()))
    durations_x = []
    for i in range(0,len(durations),3):
        a,b,c = durations[i],durations[i+1],durations[i+2]
        durations_x.append((a,b,c))
    dependencies = []
    dependency_data = list(map(int, content[2].strip().split()))
    for i in range(0, len(dependency_data), 2):
        a, b = dependency_data[i], dependency_data[i + 1]
        dependencies.append((a, b))

    return N, M, durations_x, dependencies

def triangleDist(input):
    data = []
    for i in input:
        x = random.triangular(i[0], i[2], i[1])
        data.append(round(x,2))
    return data


if __name__ == "__main__":
    processTimes = []
    num = 1000
    data = "pert.txt"
    N, M, durations_x, dependencies = readData_pertTriangle(data)

    #create graph
    g = Graph(N)
    for i in dependencies:
        g.addEdge(i[0], i[1])
    x = g.topologicalSort()

    for i in range(num):
        durations = triangleDist(durations_x)
        finalData, processTime, criticalPath = g.caluculate_Bellman(durations)
        round(processTime)
        processTimes.append(processTime)

    plt.hist(processTimes)
    plt.show()



