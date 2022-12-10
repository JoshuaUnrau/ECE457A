import math
from math import cos
from random import uniform
import matplotlib.pyplot as plt
from enum import Enum
from Queue import PriorityQueue

class G(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

class runner:
    def __init__(self):
        self.solutions = [7, 2, 3, 4, 5, 6, 1, 8]
        self.connections = [[G.B, G.C, G.D], #A
                          [G.A, G.C, G.F, G.E], #B
                          [G.A, G.D, G.G, G.F, G.E ,G.B], #C
                          [G.A, G.C ,G.G ,G.F], #D
                          [G.B, G.C, G.F, G.H], #E
                          [G.B, G.C, G.D, G.E, G.G, G.H], #F
                          [G.G, G.C, G.F, G.H], #G
                          [G.E, G.F, G.G]] #H
        self.run()

    def cost(self, solution):
        i = 0
        cost = 0
        for node in solution:
            for connection in self.connections[i]:
                # print(str(node) + " : " + str(connection) + ", "
                #       + str(solution[int(connection)]) + ", " +
                #       str(solution[int(connection)] == node + 1))
                if solution[int(connection)] == node + 1 or solution[int(connection)] == node - 1:
                    cost += 1
            i += 1
        return cost

    def swap(self, i ,j):
        solution = self.solutions[:]
        temp = solution[i]
        solution[i] = solution[j]
        solution[j] = temp
        return solution

    def get_costs(self):
        costs = PriorityQueue()
        for i in range(0, 7):
            for j in range(0, 7):
                if j > i:
                    costs.put((self.cost(self.swap(i, j)), i+1, j+1))
        return costs

    def run(self):
        #print(self.cost(self.solutions))
        #print(self.cost(1, 1))
        # Move 1
        self.solutions = [1, 2, 3, 4, 5, 6, 7, 8]
        costs = self.get_costs()
        while costs.qsize() > 0:
            print(costs.get())

        #Move 2
        self.solutions = [7, 2, 3, 4, 5, 6, 1, 8]
        costs = self.get_costs()
        while costs.qsize() > 0:
            print(costs.get())

run = runner()