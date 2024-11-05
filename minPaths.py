from graph import Graph

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
    N, data = read_file(name)
    g = Graph(N)
    durations = [N]
    for i in range(N):
        for j in range(len(data[i])):
            if(data[i][j] != 0):
                g.addEdge(i+1, j+1)
    print(g.graph)




#policzyć wszystkie drogi
#wyznaczyć nakrótsze drogi
#cel: