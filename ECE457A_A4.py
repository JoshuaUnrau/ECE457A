import math
from math import cos
from random import uniform
import matplotlib.pyplot as plt

class runner:
    def __init__(self):
        self.bounds = (-100, 100)
        self.alpha = 0.0001
        self.position = ()
        self.t_init = 1
        self.t_curr = 1
        self.cutoff = 0.05
        self.maxsteps = 10000
        self.steps = 0
        self.step_size = 1
        self.score = []
        self.visited = set()
        self.scores = dict()
        self.average_score= 0
        self.run()
        print(self.average_score/10)

    def run(self):
        temps = [0.00001, 0.0001, 0.001, 10, 100]
        for temp in temps:
            print("Temp: "+str(temp))
            self.average_score = 0
            for i in range(0, 10):
                self.anneal()
            print(self.average_score)

    def acceptance(self, new_solution):
        #Select new solution if it is better
        delta_c = self.get_score(new_solution) - self.get_score(self.position)
        #print(delta_c)
        if delta_c <= 0:
            #print(new_solution)
            #print(delta_c)
            self.position = new_solution
        else:
            p = math.e**(-delta_c / self.t_curr)
            #print(p)
            #If random is less than p select new solution
            if uniform(0, 1) < p:
                #print(new_solution)
                #print(new_solution)
                self.position = new_solution
            #Else do nothing

    def reduce_temp(self):
        self.t_curr -= self.alpha

    def reduce_temp_geo(self):
        self.t_curr *= self.alpha

    def get_new_state(self):
        #print(self.position)
        new_position = (min(max(self.bounds[0], uniform(self.position[0]-self.step_size, self.position[0]+self.step_size)), self.bounds[1]),
                       min(max(self.bounds[0], uniform(self.position[1]-self.step_size, self.position[1]+self.step_size)), self.bounds[1]))
        #print(new_position)
        #print(new_position)
        self.acceptance(new_position)
        #self.visited.add(self.position)
        #self.scores[self.position] = max(self.get_score(self.position), self.scores[self.position])

    def append_score(self):
        self.score.append(self.get_score(self.position))

    def get_score(self, position):
        x1 = position[0]
        x2 = position[1]
        return -cos(x1)*cos(x2)*math.e**(-(x1-math.pi)**2 - (x2-math.pi)**2)

    def anneal(self):
        #print(self.get_score((3,3)))
        self.score = []
        self.visited = set()
        self.scores = dict()
        self.t_curr = self.t_init
        self.position = (uniform(self.bounds[0], self.bounds[1]),
                         uniform(self.bounds[0], self.bounds[1]))
        #print(self.position)
        self.steps = 0
        while self.steps < self.maxsteps:
            self.get_new_state()
            self.append_score()
            self.reduce_temp()
            #self.reduce_temp_geo()
            self.steps += 1
        #print(self.score)
        #print(self.visited)
        #print(min(self.score))
        self.average_score += self.get_score(self.position)
        #print(self.visited)
        #print(len(self.visited))
        # # plt.scatter(visited, self.scores[],)
        # plt.plot(self.score)
        # plt.show()

run = runner()