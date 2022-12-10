import math
import sys
from math import cos
import random
import matplotlib.pyplot as plt
from Queue import PriorityQueue

#For two decimal points of accuracy
class agent:
    def __init__(self):
        self.bits = 14
        self.x = []
        self.y = []
        self.fitness = 0
        self.create()

    def create(self):
        for i in range(self.bits):
            self.x.append(random.randint(0, 1))
            self.y.append(random.randint(0, 1))

    def getDecimals(self):
        x_dec = float(int("".join(str(x) for x in self.x), 2))/1000 - 16/2
        y_dec = float(int("".join(str(y) for y in self.y), 2))/1000 - 16/2

        #Clamp values
        x_dec = min(x_dec, 5)
        x_dec = max(-5, x_dec)
        y_dec = min(y_dec, 5)
        y_dec = max(-5, y_dec)
        return x_dec, y_dec

class runner:
    def __init__(self):
        self.bits = 14
        self.agents_count = self.bits*2
        self.population = []
        self.new_population = []
        self.generations = self.agents_count
        self.pm = 1/self.bits/2
        self.pc = 0.2
        self.score = []
        self.avg_score = []
        self.run()

    def z(self, x, y):
        return (4-2.1*x**2 + (x**4)/3)*x**2 + x*y + (-4+4*y**2)*y**2

    def crossover(self, parent1, parent2):
        child1 = agent()
        child2 = agent()
        crossover_point = random.randint(0, self.bits)
        for i in range(self.bits):
            if i < crossover_point:
                child1.x[i] = parent1.x[i]
                child2.x[i] = parent2.x[i]
            else:
                child1.x[i] = parent2.x[i]
                child2.x[i] = parent1.x[i]

        crossover_point = random.randint(0, self.bits)
        for i in range(self.bits):
            if i < crossover_point:
                child1.y[i] = parent1.y[i]
                child2.y[i] = parent2.y[i]
            else:
                child1.y[i] = parent2.y[i]
                child2.y[i] = parent1.y[i]
        return child1, child2

    def selection(self, selected):
        for i in range(len(self.population)):
            k = 3
            selection = random.randint(0, len(self.population)-1)
            selection_set = []
            for i in range(k):
                selection_set.append(random.randint(0, len(self.population)-1))
            for i in selection_set:
                # check if better (e.g. perform a tournament)
                if self.population[i].fitness < self.population[selection].fitness :
                    selection = i
            #print(selection_ix)
            selected.append(self.population[selection])
        return selected

    def mutate(self, agent):
        for i in range(self.bits):
            if random.randrange(0, 1) < self.pm:
                #Swap 1 to 0 or 0 to 1
                agent.x[i] = 1 - agent.x[i]
            if random.randrange(0, 1) < self.pm:
                agent.y[i] = 1 - agent.y[i]
        return agent

    def reproduce(self):
        #Calculate fitness
        totalFitness = 0
        for agent in self.population:
            x, y = agent.getDecimals()
            agent.fitness = self.z(x,y)
            totalFitness += agent.fitness

        #Get relative fitness
        self.population.sort(key=lambda x: x.fitness, reverse=False)

        # Get best score
        print("Population size: " + str(len(self.population)))
        print("Fitness: " + str(self.population[0].fitness))
        print("Agent code" + str(self.population[0].getDecimals()))
        self.score.append(self.population[0].fitness)
        self.avg_score.append(totalFitness/self.agents_count)

        #Selection
        selected = []
        selected = self.selection(selected)
        print(len(selected))
        #print(selected)

        #Randomise population order
        #random.shuffle(self.population)

        self.new_population = []
        #Crossover (Add one half children
        i = 0
        while i < len(selected)-1:
            if random.randrange(0, 1) < self.pc and i+1 < len(selected):
                c1, c2 = self.crossover(selected[i], selected[i+1])
                self.new_population.append(c1)
                self.new_population.append(c2)
                i += 2
            else:
                self.new_population.append(selected[i])
                self.new_population.append(selected[i+1])
                i += 2

        #Refill population
        #while len(selected) < self.agents_count:


        #Mutate
        for i in range(self.agents_count):
            self.new_population[i] = self.mutate(self.new_population[i])

        print("New population size: " + str(len(self.new_population)))
        #Set population to new population
        self.population = self.new_population

    def create_agents(self):
        for i in range(self.agents_count):
            self.population.append(agent())

    def run(self):
        a = agent()
        #a.x = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # print(a.x)
        # print(a.y)
        # print(a.getDecimals())
        # print(self.z(-0.090, 0.713))
        # quit()
        self.create_agents()
        for i in range(self.generations):
            self.reproduce()
        #print(self.z())
        fig, axs = plt.subplots(2)
        fig.suptitle('Cost plots')
        axs[0].plot(self.score, color='b', label='best cost')
        plt.legend()
        axs[1].plot(self.avg_score, color='r', label='avg cost')
        plt.legend()
        plt.show()

run = runner()