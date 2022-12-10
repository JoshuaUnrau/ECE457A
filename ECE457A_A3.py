import sys
from Queue import PriorityQueue
from math import sqrt

import treelib
import pygame
from treelib import Tree

maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]]

moves = 1000
cost = 0
width = 25
height = 25

#In render y is given x and x is y

exit1 = (19, 23)
exit2 = (21, 2)
start = (11, 2)

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
PURPLE = (200, 0, 200)

# DFS order 1: 28 (2, 21)
# DFS order 2: 45 (23, 19)

# BFS order 1: 234 (2, 21)
# BFS order 2: 238 (2, 21)

class runner:
    def __init__(self):
        self.visited = set()
        self.explored = set()
        self.visitedCost = {}
        self.totalExplored = 0
        self.cost = -1 #-1 so as not to account for startinh tile
        self.queue = []
        self.priorityQueue = PriorityQueue()
        self.done = False
        self.path = []
        self.tree = Tree()
        print("Running")
        self.projectLoop()

    def get_map_cords(self, x, y):
        return y, 24-x

    def drawGrid(self):
        blockSize = 20  # Set the size of the grid block
        for x in range(0, 25):
            for y in range(0, 25):
                x_ = self.get_map_cords(x, y)[0]
                y_ = self.get_map_cords(x, y)[1]
                rect = pygame.Rect(x_ * blockSize, y_ * blockSize, blockSize, blockSize)
                if maze[x][y] == 1:
                    pygame.draw.rect(SCREEN, WHITE, rect, 1)
                elif start[0] == x and start[1] == y:
                    pygame.draw.rect(SCREEN, BLUE, rect, 1)
                elif exit1[0] == x and exit1[1] == y:
                    pygame.draw.rect(SCREEN, GREEN, rect, 1)
                elif exit2[0] == x and exit2[1] == y:
                    pygame.draw.rect(SCREEN, GREEN, rect, 1)
                elif (x, y) in self.path:
                    pygame.draw.rect(SCREEN, RED, rect, 1)
                elif (x, y) in self.explored:
                    pygame.draw.rect(SCREEN, PURPLE, rect, 1)

    def projectLoop(self):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(BLACK)

        while True:
            if not self.done:
                #DFS
                #node = self.tree.create_node(tag='start', data=start)
                #self.dfs(start, 0, node)
                # print(self.path)

                #BFS
                #self.bfs(start, 0)
                #print(self.path)

                #A*
                node = self.tree.create_node(tag='0', data=start)
                self.a_star(start, node)
                print(self.path)
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
        # while(not completed):
        # print(dfs(visited, start, 0))
        # print(visited)
        print(maze[24])
        # bfs(start, 0)

    def get_tree(self, node):
        try:
            print("Path")
            while True:
                # print(node.data)
                # print(self.cost)
                #print(node.tag)
                #print(self.tree.parent(node.identifier).data)
                self.path.append(node.data)
                node = self.tree.parent(node.identifier)
                self.cost += 1
        except:
            return

    def dfs(self, position, depth, node):
        if position not in self.visited and not self.done:
            #print(position)
            self.totalExplored += 1
            if (position == exit1 or position == exit2):
                print("Found")
                self.get_tree(node)
                print(self.cost)
                print(self.totalExplored)
                print(position)
                self.done = True
                print("Done")
            self.visited.add(position)
            for new_position in self.getMoves_order1(position):
                new_node = self.tree.create_node(tag=''+str(depth), data=new_position, parent=node)
                self.dfs(new_position, depth + 1, new_node)

    def bfs(self, position, depth):
        self.visited.add(position)
        node = self.tree.create_node(tag='start', data=position)
        self.queue.append((position, node))
        while len(self.queue) > 0 and not self.done:
            position, node = self.queue.pop(0)
            depth += 1
            for new_position in self.getMoves_order1(position):
                if (new_position == exit1 or new_position == exit2):
                    print("Found")
                    goal_node = self.tree.create_node(tag='' + str(depth), data=new_position, parent=node)
                    self.get_tree(goal_node)
                    print(self.cost)
                    print(self.totalExplored)
                    self.done = True
                    print("Done")
                    break
                if new_position not in self.visited:
                    self.totalExplored += 1
                    new_node = self.tree.create_node(tag='' + str(depth), data=new_position, parent=node)
                    self.visited.add(new_position)
                    self.queue.append((new_position, new_node))
        # print("Visited")

    def a_star(self, position, node):
        self.visited.add(position)
        self.visitedCost[position] = int(node.tag)
        #Priority queue is order based on first object
        self.priorityQueue.put((self.manhattan_distance(position), position, node))
        previous_node = node
        while self.priorityQueue.qsize() > 0 and not self.done:
            distance, position, node = self.priorityQueue.get()
            self.totalExplored += 1
            self.explored.add(position)
            if (position == exit1 or position == exit2):
                print("Found")
                self.get_tree(node)
                print(position)
                print(self.cost)
                print(self.totalExplored)
                self.done = True
                print("Done")
                break
            for new_position in self.getMoves_order1(position):
                cost = int(node.tag) + 1
                revisit = False
                if new_position in self.visited:
                    # print(self.visited)
                    # print(self.visitedCost)
                    if self.visitedCost[new_position] > cost:
                        revisit = True
                if new_position not in self.visited or revisit:
                    #print("Cost")
                    # print(cost)
                    # print(self.manhattan_distance(new_position))
                    #print(self.manhattan_distance(new_position)+cost)
                    new_node = self.tree.create_node(tag='' + str(cost), data=new_position, parent=node)
                    self.visited.add(new_position)
                    self.visitedCost[new_position] = int(node.tag)
                    self.priorityQueue.put((self.manhattan_distance(new_position)+cost, new_position, new_node))

    def distance(self, point1, point2):
        return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

    def manhattan_distance(self, position):
        return min(self.distance(position, exit1), self.distance(position, exit2))

    # In render y is given x and x is y
    def getMoves_order1(self, position):
        moves = []
        #Left
        if self.canMove((position[0], position[1] - 1)):
            moves.append((position[0], position[1] - 1))
        #Up
        if self.canMove((position[0] + 1, position[1])):
            moves.append((position[0] + 1, position[1]))
        #Right
        if self.canMove((position[0], position[1] + 1)):
            moves.append((position[0], position[1] + 1))
        #Down
        if self.canMove((position[0] - 1, position[1])):
            moves.append((position[0] - 1, position[1]))
        return moves

    def getMoves_order2(self, position):
        moves = []
        #Right
        if self.canMove((position[0], position[1] + 1)):
            moves.append((position[0], position[1] + 1))
        #Up
        if self.canMove((position[0] + 1, position[1])):
            moves.append((position[0] + 1, position[1]))
        #Left
        if self.canMove((position[0], position[1] - 1)):
            moves.append((position[0], position[1] - 1))
        #Down
        if self.canMove((position[0] - 1, position[1])):
            moves.append((position[0] - 1, position[1]))
        return moves

    def canMove(self, position):
        # print("cant move")
        # print(position)
        # print(maze[position[0]][position[1]])
        # Maze x and y axises are flipped
        return not (position[0] < 0 or position[0] >= width or position[1] < 0 or position[1] >= height
                    or maze[position[0]][position[1]] == 1)


runner = runner()