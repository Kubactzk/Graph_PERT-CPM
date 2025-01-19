import random
import math
import time
import copy
import matplotlib.pyplot as plt

def generateData(num):
    points = []
    for i in range(num):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        points.append((x, y))
    return points

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(tour):
    dist = 0
    for i in range(len(tour)):
        dist += calculate_distance(tour[i], tour[(i + 1) % len(tour)])
    return dist

def NN(points):
    points = list(points)
    start = points[0]
    tour = [start]
    unvisited = set(points[1:])

    while unvisited:
        current = tour[-1]
        next_point = min(unvisited, key=lambda point: calculate_distance(current, point))
        tour.append(next_point)
        unvisited.remove(next_point)

    return tour

def FI(points):
    points = list(points)
    start = points[0]
    tour = [start, points[1]]
    points = points[2:]

    while points:
        farthest_point = max(points, key=lambda p: min(calculate_distance(p, t) for t in tour))
        best_position = 0
        min_increase = float('inf')

        for i in range(len(tour)):
            increase = (calculate_distance(tour[i], farthest_point) +
                        calculate_distance(farthest_point, tour[(i + 1) % len(tour)]) - 
                        calculate_distance(tour[i], tour[(i + 1) % len(tour)]))
            if increase < min_increase:
                min_increase = increase
                best_position = i + 1

        tour.insert(best_position, farthest_point)
        points.remove(farthest_point)

    return tour

def two_opt(tour):
    best = tour
    improved = True
    distances = [total_distance(tour)]  # Track improvement per iteration
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                if j - i == 1:  # Consecutive segments, skip
                    continue
                new_tour = best[:i] + best[i:j][::-1] + best[j:]
                if total_distance(new_tour) < total_distance(best):
                    best = new_tour
                    distances.append(total_distance(best))
                    improved = True
    return best, distances

def plot_initial_route(points, title):
    """Plot the initial random route before optimization."""
    x = [point[0] for point in points] + [points[0][0]]
    y = [point[1] for point in points] + [points[0][1]]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='r')
    plt.grid()
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig(f"{title}.png")
    plt.show()

def plot_tour(tour, title):
    """Plot the final optimized tour."""
    x = [point[0] for point in tour] + [tour[0][0]]
    y = [point[1] for point in tour] + [tour[0][1]]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.grid()
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig(f"{title}.png")
    plt.show()

def plot_improvement(distances, title):
    """Plot the improvement in the tour's total distance after applying 2-opt."""
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(distances)), distances, marker='o', linestyle='-', color='g')
    plt.grid()
    plt.title(title)
    plt.xlabel('Iteration')
    plt.ylabel('Total Distance')
    plt.savefig(f"{title}.png")
    plt.show()

def plot_combined_improvement(no_opt_distances, opt_distances, title):
    """Plot combined improvement for both with and without 2-opt."""
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(no_opt_distances)), no_opt_distances, marker='o', linestyle='-', color='r', label='Without 2-opt')
    opt_start_idx = len(no_opt_distances) - 1
    opt_iterations = list(range(opt_start_idx, opt_start_idx + len(opt_distances)))
    plt.plot(opt_iterations, opt_distances, marker='o', linestyle='-', color='b', label='With 2-opt')
    plt.grid()
    plt.title(title)
    plt.xlabel('Iteration')
    plt.ylabel('Total Distance')
    plt.legend()
    plt.savefig(f"{title}.png")
    plt.show()

def plot_comparison(no_opt_distance, opt_distance, title):
    """Plot a bar chart comparison of distances before and after 2-opt."""
    plt.figure(figsize=(10, 6))
    plt.bar(["Without 2-opt", "With 2-opt"], [no_opt_distance, opt_distance], color=['red', 'blue'])
    plt.grid()
    plt.title(title)
    plt.ylabel('Total Distance')
    plt.savefig(f"{title}.png")
    plt.show()

if __name__ == "__main__":
    points = set(generateData(1000))

    # Plot the initial random route
    plot_initial_route(list(points), "Initial Random Route")

    # Performance measurement for NN
    start_time = time.time()
    nn_tour = NN(points)
    nn_time = time.time() - start_time
    nn_distance = total_distance(nn_tour)
    print(f"Nearest Neighbor Distance: {nn_distance}")
    print(f"Nearest Neighbor Execution Time: {nn_time:.4f} seconds")
    # plot_tour(nn_tour, "Nearest Neighbor Tour")

    # Apply 2-opt to NN solution
    start_time = time.time()
    nn_tour_optimized, nn_distances = two_opt(nn_tour)
    nn_2opt_time = time.time() - start_time
    nn_distance_optimized = total_distance(nn_tour_optimized)
    print(f"Nearest Neighbor Distance (2-opt): {nn_distance_optimized}")
    print(f"Nearest Neighbor 2-opt Execution Time: {nn_2opt_time:.4f} seconds")
    # plot_tour(nn_tour_optimized, "Nearest Neighbor Tour (2-opt)")
    # plot_combined_improvement([nn_distance] * len(nn_distances), nn_distances, "Nearest Neighbor Combined Improvement")
    # plot_comparison(nn_distance, nn_distance_optimized, "Nearest Neighbor Distance Comparison")

    # Performance measurement for FI
    start_time = time.time()
    fi_tour = FI(points)
    fi_time = time.time() - start_time
    fi_distance = total_distance(fi_tour)
    print(f"Farthest Insertion Distance: {fi_distance}")
    print(f"Farthest Insertion Execution Time: {fi_time:.4f} seconds")
    # plot_tour(fi_tour, "Farthest Insertion Tour")

    # Apply 2-opt to FI solution
    start_time = time.time()
    fi_tour_optimized, fi_distances = two_opt(fi_tour)
    fi_2opt_time = time.time() - start_time
    fi_distance_optimized = total_distance(fi_tour_optimized)
    print(f"Farthest Insertion Distance (2-opt): {fi_distance_optimized}")
    print(f"Farthest Insertion 2-opt Execution Time: {fi_2opt_time:.4f} seconds")
    # plot_tour(fi_tour_optimized, "Farthest Insertion Tour (2-opt)")
    # plot_combined_improvement([fi_distance] * len(fi_distances), fi_distances, "Farthest Insertion Combined Improvement")
    # plot_comparison(fi_distance, fi_distance_optimized, "Farthest Insertion Distance Comparison")
