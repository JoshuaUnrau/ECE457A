import math
import scipy.io
import random
import numpy as np
import matplotlib.pyplot as plt

mat = scipy.io.loadmat('Ex1_data_RANSAC.mat')

temp = mat['data']
temp.astype(np.float)
data = []

#Used to gather the data from the file and format it
for point in temp:
    try:
        f_point = [float(point[0]),float(point[1])]
        data.append(f_point)
    except:
        pass

#Calculates the distance between points
def dist(point1, point2):
    try:
        x1 = point1[0]
        x2 = point2[0]
        y1 = point1[1]
        y2 = point2[1]
        #print(point1)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    except:
        pass
        # print(point1)
        # print(point2)

#s_a = [100, 1000, 2000]
#t_a = [0.1, 0.2, 0.3]

#Settings for samples and thresholds
s_a = [2000]
t_a = [0.3]
for s in s_a:
    for t in t_a:

        #holds the data for the best points
        best_point1 = data[0]
        best_point2 = data[1]
        best_radius = 0
        best_amount = 0
        best_amounts = []

        for i in range(s):
            # Randomly shuffle the data
            random.shuffle(data)

            #Get Two Points
            point1 = data[0]
            point2 = data[1]

            #Get points distances
            radius = dist(point1, point2)
            set = []
            for point in temp:
                if(dist(point1, point) < radius + t and dist(point1, point) > radius - t):
                   set.append(point)
            #If a better solution record it
            if len(set) > best_amount:
                best_point1 = point1
                best_point2 = point2
                best_amount = len(set)
                best_amounts.append(best_amount)
                best_radius = radius


        print(best_point1)
        print(best_point2)
        print(best_amount)
        x = []
        y = []
        for point in temp:
            x.append(point[0])
            y.append(point[1])

        #Plot the circle and points
        circle1 = plt.Circle((best_point1[0], best_point1[1]), best_radius, color='r', fill=False)
        fig, axs = plt.subplots(2)
        fig.set_dpi(200)
        fig.suptitle('S =' + str(s) + ' Threshold = ' + str(t))
        axs[0].scatter(x, y, color='b', label='points')
        axs[0].add_patch(circle1)
        plt.legend()

        axs[1].plot(best_amounts, color='r', label='best')
        plt.legend()
        plt.show()

