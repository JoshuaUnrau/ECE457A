import math
import sys
from math import cos
import random
import matplotlib.pyplot as plt

#For two decimal points of accuracy
class particle:
    def __init__(self):
        self.pos = [0, 0]
        self.vel = [0, 0]
        self.pBestPos = [0, 0]
        self.pBest = 999
        self.cost = 999
        self.fitness = 0
        self.create()

    def create(self):
        min_bound = -5
        max_bound = 5
        self.pos[0] = (random.randint(min_bound, max_bound))
        self.pos[1] = (random.randint(min_bound, max_bound))
        self.pBestPos[0] = (random.randint(min_bound, max_bound))
        self.pBestPos[1] = (random.randint(min_bound, max_bound))

class runner:
    def __init__(self):
        self.bounds = [-5, 5]
        self.particles = []
        self.particles_count = 100
        self.score = []
        self.w = 0.1
        self.c1 = 1
        self.c2 = 1
        # self.r1 = random.randrange(0, 1)
        # self.r2 = random.randrange(0, 1)
        self.r1 = 1/2
        self.r2 = 1/2
        self.speed = 0.1
        self.iterations = 200
        self.nBestPos = [0, 0]
        self.nBest = 999
        self.avg_score = 999
        self.avg_scores = []
        self.run()

    def update(self, particle):
        #Update particle velocity
        particle.vel[0] = self.w*particle.vel[0] + \
                          self.c1 * self.r1 * (particle.pBestPos[0] - particle.pos[0]) + \
                          self.c2 * self.r1 * (self.nBestPos[0] - particle.pos[0])
        particle.vel[1] = self.w * particle.vel[1] + \
                          self.c1 * self.r1 * (particle.pBestPos[1] - particle.pos[1]) + \
                          self.c2 * self.r1 * (self.nBestPos[1] - particle.pos[1])

        #Update particle position
        particle.pos[0] += particle.vel[0]*self.speed
        particle.pos[1] += particle.vel[1]*self.speed

        #Bound position to map bounds
        if particle.pos[0] > 5:
            particle.pos[0] = 5
        if particle.pos[0] < -5:
            particle.pos[0] = -5
        if particle.pos[1] > 5:
            particle.pos[1] = 5
        if particle.pos[1] < -5:
            particle.pos[1] = -5

        #Set local and global costs
        cost = self.z(particle.pos[0], particle.pos[1])
        particle.cost = cost
        self.avg_score += cost
        if cost < particle.pBest:
            particle.pBestPos = particle.pos
            particle.pBest = cost
        if cost < self.nBest:
            self.nBest = cost
            self.nBestPos = particle.pos

    def z(self, x, y):
        #print("X: "+str(x)+ " Y: "+str(y))
        return (4 - 2.1 * x ** 2 + (x ** 4) / 3) * x ** 2 + x * y + (-4 + 4 * y ** 2) * y ** 2

    def initialise(self):
        min_bound = self.bounds[0]
        max_bound = self.bounds[1]
        self.nBestPos[0] = (random.randint(min_bound, max_bound))
        self.nBestPos[1] = (random.randint(min_bound, max_bound))
        for i in range(0, self.particles_count):
            p = particle()
            self.particles.append(p)

    def run(self):
        self.initialise()
        for i in range(self.iterations):
            self.avg_score = 0
            for particle in self.particles:
                self.update(particle)
            self.avg_score /= self.particles_count
            self.score.append(self.nBest)
            self.avg_scores.append(self.avg_score)

        #Plot results
        fig, axs = plt.subplots(2)
        fig.suptitle('Cost plots')
        print(self.nBestPos)
        print(self.nBest)
        axs[0].plot(self.score, color='b', label='best cost')
        plt.legend()
        axs[1].plot(self.avg_scores, color='r', label='avg cost')
        plt.legend()
        plt.show()

run = runner()