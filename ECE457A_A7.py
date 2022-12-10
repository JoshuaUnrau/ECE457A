import math
import sys
from math import cos
import numpy as np
import random
import matplotlib.pyplot as plt
import csv

city_cord = []
cities = []

with open('Assignment7-city coordinates.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    i = 0
    for row in spamreader:
        if i != 0:
            #print(row[0].split(","))
            vals = row[0].split(",")
            city_cord.append((int(vals[1]), int(vals[2])))
            cities.append(i-1)
        i += 1

print(city_cord)
print(cities)
print(len(cities))

class Ant:
    def __init__(self):
        self.location = 0
        self.solution_cost = 0
        self.visited = []


class runner:
    def __init__(self):
        self.ant_amount = 50
        self.evap_rate = 0.99
        self.iterations = 1000
        self.alpha = 1
        self.beta = 10
        self.ants = []
        self.trails = []
        self.new_trails = []
        self.city_weights = []
        self.run()

    def selectAntPath(self, ant):
        city_weights_list = self.city_weights.copy()
        visited_slots = [1] * len(city_weights_list)
        visited_slots[0] = 0
        ant.visited.append(0)
        while len(ant.visited) < len(cities):
            #Weighted choice
            weights = np.multiply(city_weights_list[ant.location],visited_slots)

            #Select the next spot using a weighted average
            choice = random.choices(cities, weights=weights)[0]

            #Add this spot to the list of visited places
            ant.visited.append(choice)

            #Dont revist this spot
            visited_slots[choice] = 0

            #Add trail to the new trails array
            self.new_trails[ant.location][choice] += 1
            #print(choice)
            #Add the distance traveled
            ant.solution_cost += self.distance(ant.location, choice)
            ant.location = choice
        #Final step return to home
        ant.solution_cost += self.distance(ant.location, 0)
        ant.location = 0
        ant.visited.append(0)
        # #Update trails
        # for i in range(1, len(ant.visited)):
        #     i = ant.visited[i-1]
        #     j = ant.visited[i]
        #     self.new_trails[i][j] += 1#/ant.solution_cost
        #print(self.new_trails)

    def updatePheromones(self):
        for i in range(0, len(city_cord)):
            for j in range(0, len(city_cord)):
                #Evaporate trail
                self.trails[i][j] *= self.evap_rate
                #Apply new trails
                self.trails[i][j] += self.new_trails[i][j]
                #Clear the new trails array
                self.new_trails[i][j] = 0

    def distance(self, i, j):
        return math.sqrt((city_cord[i][0]-city_cord[j][0])**2 + (city_cord[i][1]-city_cord[j][1])**2)

    def updateCityWeights(self):
        for i in range(0, len(city_cord)):
            for j in range(0, len(city_cord)):
                if i == j:
                    self.city_weights[i][j] = 0
                else:
                    self.city_weights[i][j] = (self.trails[i][j]**self.alpha)/(self.distance(i,j)**self.beta)

    def run(self):
        best_cost = 99999999
        best_solution = []
        costs = []
        average_fitness = []

        #Test distance
        print(self.distance(0, 1))
        assert self.distance(0, 1) == 529.5280917949491

        #Set default array values
        for i in range(0, len(city_cord)):
            self.trails.append([])
            self.new_trails.append([])
            self.city_weights.append([])
            for j in range(0, len(city_cord)):
                self.trails[i].append(1)
                self.city_weights[i].append(1)
                self.new_trails[i].append(0)

        for i in range(0, self.ant_amount):
            ant = Ant()
            self.ants.append(ant)
        for i in range(self.iterations):
            self.updatePheromones()
            self.updateCityWeights()
            average_fitness_val = 0
            for ant in self.ants:
                self.selectAntPath(ant)
                #print(ant.solution_cost)
                if ant.solution_cost < best_cost:
                    best_cost = ant.solution_cost
                    best_solution = ant.visited
                average_fitness_val += ant.solution_cost
                ant.solution_cost = 0
                ant.visited = []
                ant.location = 0
            average_fitness_val /= len(self.ants)
            average_fitness.append(average_fitness_val)
            costs.append(best_cost)

        #Plots
        fig, axs = plt.subplots(3)
        fig.suptitle('Cost plots')
        axs[0].plot(costs, color='b', label='best cost')
        plt.legend()
        axs[1].plot(average_fitness, color='r', label='avg cost')
        plt.legend()

        x = []
        y = []
        for point in city_cord:
            x.append(point[0])
            y.append(point[1])
        axs[2].plot(x, y, 'co')
        for _ in range(1, len(best_solution)):
            i = best_solution[_ - 1]
            j = best_solution[_]
            plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)
        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)

        print(best_solution)
        print(best_cost)
        plt.show()

run = runner()