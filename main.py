import math
import random
import time
import numpy as np

file = "tsp_10.txt"
###############################################################################
'''Read data into a matrix'''


def nrOfVertexes(file):
    return int(open(file, "r").readline())


def costOfEdges(file):
    rows = open(file, "r").read().splitlines()
    cost_of_edges = []
    for r in range(1, nrOfVertexes(file) + 1):
        cost_of_edges.append(rows[r].split())
    return cost_of_edges


###############################################################################
'''Smiluated Annealing'''


# Define the distance matrix
# dist_matrix = np.array([[0, 5, 6, 4, 10, 5, 9, 8, 7, 5],
#                         [5, 0, 5, 7, 8, 3, 4, 6, 3, 3],
#                         [6, 5, 0, 8, 9, 5, 6, 4, 7, 5],
#                         [4, 7, 8, 0, 6, 7, 5, 4, 6, 7],
#                         [10, 8, 9, 6, 0, 9, 5, 8, 7, 9],
#                         [5, 3, 5, 7, 9, 0, 7, 5, 4, 5],
#                         [9, 4, 6, 5, 5, 7, 0, 8, 4, 3],
#                         [8, 6, 4, 4, 8, 5, 8, 0, 5, 6],
#                         [7, 3, 7, 6, 7, 4, 4, 5, 0, 4],
#                         [5, 3, 5, 7, 9, 5, 3, 6, 4, 0]])
dist_matrix = costOfEdges(file)

N = 10

T = 100         # initial temperature
Tmin = 0.001    # minimum temperature
alpha = 0.99    # cooling rate

# Generate a random solution
solution = [random.randint(0, N-1) for x in range(N)]

# Calculate the initial cost
cost = 0
for i in range(N-1):
    cost += dist_matrix[solution[i]][solution[i+1]]


def simulatedAnnealing(t, s, c):
    while t > Tmin:
        # Generate a random successor
        new_s = list(s)
        while True:
            i, j = random.randint(0, N - 1), random.randint(0, N - 1)
            if i != j:
                break
        new_s[i], new_s[j] = new_s[j], new_s[i]

        # Calculate the new cost
        new_c = 0
        for i in range(N - 1):
            new_c += dist_matrix[new_s[i]][new_s[i + 1]]

        # Decide whether to accept the new solution
        if new_c < c:
            c = new_c
            s = new_s
        else:
            p = math.exp((c - new_c) / t)
            if random.random() < p:
                c = new_c
                s = new_s

        # Cooling
        t *= alpha


###############################################################################
'''Timing'''


def readFromIni(file):
    file = open(file, "r")
    rows = file.read().splitlines()
    data = []
    for r in range(1, len(rows)):
        data.append(rows[r].split())
    return data


def calculateDifference(file, repeat, csv_file):
    for r in range(repeat):
        start = time.time_ns()
        for r2 in range(10):
            simulatedAnnealing(costOfEdges(file), file)
        end = time.time_ns()
        difference = end - start
        csv_file.write(str(difference / 10) + "\n")


def timingOneFile(file, repeat, csv_file):
    for r in range(int(repeat)):
        start = time.time_ns()
        simulatedAnnealing(costOfEdges(file), file)
        end = time.time_ns()
        difference = end - start
        csv_file.write(str(difference) + "\n")
    if file == "tsp_6_1.txt" or file == "tsp_6_2.txt":
        calculateDifference(file, repeat, csv_file)
    else:
        for r in range(int(repeat)):
            start = time.time_ns()
            simulatedAnnealing(costOfEdges(file), file)
            end = time.time_ns()
            difference = end - start
            csv_file.write(str(difference) + "\n")


def checkingFiles(file):
    csv_file = open("test_atsp_out.csv", "w")
    data = readFromIni(file)
    nr_of_files = len(data)
    for nr_of_file in range(nr_of_files):
        file_name = str(data[nr_of_file][0])
        repeat = int(data[nr_of_file][1])
        csv_file.write(str(data[nr_of_file]) + "\n")
        timingOneFile(file_name, repeat, csv_file)


if __name__ == "__main__":
    pass
    # checkingFiles("porownanie.ini")
