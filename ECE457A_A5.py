import math
import sys
from math import cos
import random
import matplotlib.pyplot as plt
from Queue import PriorityQueue

class runner:
    def __init__(self):
        self.flow = [
                [0, 0, 5, 0, 5, 2, 10, 3, 1, 5, 5, 5, 0, 0, 5, 4, 4, 0, 0, 1],
                [0, 0, 3, 10, 5, 1, 5, 1, 2, 4, 2, 5, 0, 10, 10, 3, 0, 5, 10, 5],
                [5, 3, 0, 2, 0, 5, 2, 4, 4, 5, 0, 0, 0, 5, 1, 0, 0, 5, 0, 0],
                [0, 10, 2, 0, 1, 0, 5, 2, 1, 0, 10, 2, 2, 0, 2, 1, 5, 2, 5, 5],
                [5, 5, 0, 1, 0, 5, 6, 5, 2, 5, 2, 0, 5, 1, 1, 1, 5, 2, 5, 1],
                [2, 1, 5, 0, 5, 0, 5, 2, 1, 6, 0, 0, 10, 0, 2, 0, 1, 0, 1, 5],
                [10, 5, 2, 5, 6, 5, 0, 0, 0, 0, 5, 10, 2, 2, 5, 1, 2, 1, 0, 10],
                [3, 1, 4, 2, 5, 2, 0, 0, 1, 1, 10, 10, 2, 0, 10, 2, 5, 2, 2, 10],
                [1, 2, 4, 1, 2, 1, 0, 1, 0, 2, 0, 3, 5, 5, 0, 5, 0, 0, 0, 2],
                [5, 4, 5, 0, 5, 6, 0, 1, 2, 0, 5, 5, 0, 5, 1, 0, 0, 5, 5, 2],
                [5, 2, 0, 10, 2, 0, 5, 10, 0, 5, 0, 5, 2, 5, 1, 10, 0, 2, 2, 5],
                [5, 5, 0, 2, 0, 0, 10, 10, 3, 5, 5, 0, 2, 10, 5, 0, 1, 1, 2, 5],
                [0, 0, 0, 2, 5, 10, 2, 2, 5, 0, 2, 2, 0, 2, 2, 1, 0, 0, 0, 5],
                [0, 10, 5, 0, 1, 0, 2, 0, 5, 5, 5, 10, 2, 0, 5, 5, 1, 5, 5, 0],
                [5, 10, 1, 2, 1, 2, 5, 10, 0, 1, 1, 5, 2, 5, 0, 3, 0, 5, 10, 10],
                [4, 3, 0, 1, 1, 0, 1, 2, 5, 0, 10, 0, 1, 5, 3, 0, 0, 0, 2, 0],
                [4, 0, 0, 5, 5, 1, 2, 5, 0, 0, 0, 1, 0, 1, 0, 0, 0, 5, 2, 0],
                [0, 5, 5, 2, 2, 0, 1, 2, 0, 5, 2, 1, 0, 5, 5, 0, 5, 0, 1, 1],
                [0, 10, 0, 5, 5, 1, 0, 2, 0, 5, 2, 2, 0, 5, 10, 2, 2, 1, 0, 6],
                [1, 5, 0, 5, 1, 5, 10, 10, 2, 2, 5, 5, 5, 0, 10, 0, 0, 1, 6, 0]]

        self.distance = [
                    [0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 2, 3, 4, 5, 6, 3, 4, 5, 6, 7],
                    [1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4, 5, 4, 3, 4, 5, 6],
                    [2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4, 5, 4, 3, 4, 5],
                    [3, 2, 1, 0, 1, 4, 3, 2, 1, 2, 5, 4, 3, 2, 3, 6, 5, 4, 3, 4],
                    [4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3],
                    [1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 2, 3, 4, 5, 6],
                    [2, 1, 2, 3, 4, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4, 5],
                    [3, 2, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4],
                    [4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 4, 3, 2, 1, 2, 5, 4, 3, 2, 3],
                    [5, 4, 3, 2, 1, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2],
                    [2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 1, 2, 3, 4, 5],
                    [3, 2, 3, 4, 5, 2, 1, 2, 3, 4, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4],
                    [4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3],
                    [5, 4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 4, 3, 2, 1, 2],
                    [6, 5, 4, 3, 2, 5, 4, 3, 2, 1, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1],
                    [3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4],
                    [4, 3, 4, 5, 6, 3, 2, 3, 4, 5, 2, 1, 2, 3, 4, 1, 0, 1, 2, 3],
                    [5, 4, 3, 4, 5, 4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 2],
                    [6, 5, 4, 3, 4, 5, 4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1],
                    [7, 6, 5, 4, 3, 6, 5, 4, 3, 2, 5, 4, 3, 2, 1, 4, 3, 2, 1, 0]]

        self.T = 20
        self.size = 20
        #Could make these the same matrix but simpler to code if separate
        self.tabu_matrix_recency = [([0] * self.size) for i in range(self.size)]
        self.tabu_matrix_frequency = [([0] * self.size) for i in range(self.size)]
        self.max_iters = 10**3
        self.iters = 0
        self.score = []
        self.score_t = []
        self.no_improvement_iters = 0
        self.solutions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        #Modifiers
        self.use_aspiration = False
        self.randomSearch = False
        self.frequencySearch = True

        self.run()


    def cost(self, solution):
        cost = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                #Flow is always the same between departments
                #Distance varies using solution array
                cost += self.flow[solution[i]][solution[j]]*self.distance[i][j]
        return cost

    def swap(self, i, j):
        solution = self.solutions[:]
        temp = solution[i]
        solution[i] = solution[j]
        solution[j] = temp
        return solution

    def get_costs(self):
        costs = PriorityQueue()
        for i in range(0, self.size):
            for j in range(0, self.size):
                if j > i:
                    if not self.randomSearch or random.randint(1, 2) == 1:
                        #print(str(i) + ", " + str(j))
                        if self.frequencySearch:
                            costs.put((self.cost(self.swap(i, j)) + self.tabu_matrix_frequency[i][j], i, j))
                        else:
                            costs.put((self.cost(self.swap(i, j)), i, j))
        return costs

    def stop(self):
        return self.no_improvement_iters > 5 or self.iters > self.max_iters

    def update_tabu(self, i_, j_):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.tabu_matrix_recency[i][j] > 0:
                    self.tabu_matrix_recency[i][j] -= 1
        self.tabu_matrix_recency[i_][j_] = self.T
        if self.frequencySearch:
            self.tabu_matrix_frequency[i_][j_] += 1

    def run(self):
        done = False
        min_cost = sys.maxint
        #random.shuffle(self.solutions)
        print(self.solutions)
        print(self.T)
        while not done:
            costs = self.get_costs()
            i, j = 0, 0
            real_cost = sys.maxint

            #Get the best tabu option
            while costs.qsize() > 0:
                cost, i, j = costs.get()
                # If not in recency tabu table select
                if self.tabu_matrix_recency[i][j] == 0:
                    real_cost = cost - self.tabu_matrix_frequency[i][j]
                    break

            costs = self.get_costs()
            #Search for the lowest cost
            if self.use_aspiration:
                while costs.qsize() > 0:
                    cost, i_temp, j_temp = costs.get()
                    #Search for a best solution so far
                    if min_cost > cost - self.tabu_matrix_frequency[i][j]:
                        min_cost = cost - self.tabu_matrix_frequency[i][j]
                        real_cost = cost - self.tabu_matrix_frequency[i][j]
                        i = i_temp
                        j = j_temp
            else:
                if real_cost < min_cost:
                    min_cost = real_cost


            #Stop?
            if self.stop():
                break

            #increment solution
            self.iters += 1
            self.solutions = self.swap(i, j)
            self.update_tabu(i, j)
            #print((real_cost, i, j, self.solutions))
            self.score.append(real_cost)
        plt.plot(self.score, color='b', label='cost')
        #plt.plot(self.score_t, color='r', label='tabu_cost')
        plt.legend()
        plt.show()
        print(min_cost)

run = runner()