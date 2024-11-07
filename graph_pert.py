from graph import Graph
import random
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis
import numpy as np


def readData_pertTriangle(path):
    with open(path, 'r') as file:
        # Read the entire file content
        content = file.read().splitlines()
    N, M = map(int, content[0].split())
    X, Y = map(int, content[4].split())
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

    return N, M, X, Y, durations_x, dependencies

def Pert(durations_x):
    t_oper = []
    sigma_squared = []
    for item in durations_x:
        t = (item[0]+4*item[1]+item[2])/6
        sigma = (item[2]-item[0])/6
        t_oper.append(round(t,2))
        sigma_squared.append(round(pow(sigma,2),2))
    return t_oper, sigma_squared

def plotHist(data,iterations,num_bins, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    sns.histplot(data, bins=num_bins, kde=True, color='g', edgecolor="black")
    plt.show()
    plt.savefig(f"{iterations}.png")
    plt.close()

def triangleDist(input):
    data = []
    for i in input:
        x = random.triangular(i[0], i[2], i[1])
        data.append(round(x,2))
    return data


if __name__ == "__main__":
    data = "pert.txt"
    N, M, X, Y, durations_x, dependencies = readData_pertTriangle(data)
    durations_pert, sigma_squared = Pert(durations_x)
    g_pert = Graph(N)
    for i in dependencies:
        g_pert.addEdge(i[0], i[1])
    x_pert = g_pert.topologicalSort()

    finalData, processTime_pert, criticalPath = g_pert.caluculate_Bellman(durations_pert)
    criticalPath_pert = []
    project_sigma = 0
    for item in criticalPath:
        idx = item[0]
        criticalPath_pert.append(idx)
        project_sigma += sigma_squared[idx-1]
    project_sigma = round(pow(project_sigma,0.5),2)

    probabilityX = round(norm.cdf((X - processTime_pert)/project_sigma),2)
    timeY = processTime_pert + project_sigma * round(norm.ppf(Y/100),2)
    print("=====================PERT==========================")
    print(f"Critical path: {criticalPath_pert}")
    print("Expected finish time, standard deviation:", processTime_pert, project_sigma)
    print("Probability in ending X sequence:", probabilityX)
    print("Project will end in 99% in days:", round(timeY,2))

    # Triangle dist
    processTimes = []
    num = 100000

    #create graph
    g = Graph(N)
    for i in dependencies:
        g.addEdge(i[0], i[1])
    x = g.topologicalSort()
    for i in range(num):
        durations = triangleDist(durations_x)
        finalData, processTime, criticalPath = g.caluculate_Bellman(durations)
        processTimes.append(processTime)
    simProbs = []

    for sample in range(13, 24):
        counter = 0
        for i in processTimes:
            if (i <= sample):
                counter += 1
        simProbs.append(round((counter/len(processTimes))*100, 3))
    print("===========================TRIANGLE SIMULATION===========================")
    print(simProbs)
    titleSim = f"PERT triangular simulation in {num} iterations"
    xlabelSim = "Process time [days]"
    ylabelSim = "Number of samples"

    # Freedmana-Diaconis - wyliczenie bins na histogramie
    iqr = np.percentile(processTimes, 75) - np.percentile(processTimes, 25)
    bin_width = 2 * iqr / (len(processTimes) ** (1 / 3))
    num_bins = int((max(processTimes) - min(processTimes)) / bin_width)


    min_value = np.min(processTimes)
    max_value = np.max(processTimes)
    mean_value = np.mean(processTimes)
    median_value = np.median(processTimes)
    std_dev = np.std(processTimes)
    asymmetry = skew(processTimes)
    peakness = kurtosis(processTimes, fisher=False)
    print("Minimalny czas:", min_value)
    print("Maksymalny czas:", max_value)
    print("Średni czas:", mean_value)
    print("Mediana:", median_value)
    print("Odchylenie standardowe:", std_dev)
    print("Wskaźnik asymetrii (Skewness):", asymmetry)
    print("Kurtoza (Kurtosis):", peakness)

    plotHist(processTimes, num, num_bins, titleSim, xlabelSim, ylabelSim)