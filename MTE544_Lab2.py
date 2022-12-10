import math
import random
import numpy as np
from itertools import chain
import matplotlib.pyplot as plt

map = np.loadtxt('test.txt')

print(map)
for i in range(0, len(map)):
    for j in range(0, len(map[i])):
        if map[i][j] > 200:
            map[i][j] = 254
# plt.imshow(map)
# #plt.gray()
# plt.show()


#make the map bigger
bigger_map = []
offset = 300
for i in range(0, offset*2):
    bigger_map.append([])
    for j in range(0, offset*2):
        bigger_map[i].append(254)
print(bigger_map)
for i in range(0, len(map)):
    for j in range(0, len(map[i])):
        # print(bigger_map[i][j])
        # print(int(map[i][j]))
        bigger_map[i+int(offset/4)][j+int(offset/2)] = int(map[i][j])
plt.imshow(bigger_map)
#plt.gray()
plt.show()

map = bigger_map
#This might be different from ros global cords (Doesnt matter?)
x_range = [0, 200]
y_range = [0, 300]
angle_range = [0, 2*math.pi]
sensor_range = 50
sensor_fov = math.pi/2

#https://rosettacode.org/wiki/Bitmap/Midpoint_circle_algorithm#Python
def circle(x0, y0, radius):
    points = []
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    points.append((x0, y0 + radius))
    points.append((x0, y0 - radius))
    points.append((x0 + radius, y0))
    points.append((x0 - radius, y0))

    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x
        points.append((x0 + x, y0 + y))
        points.append((x0 - x, y0 + y))
        points.append((x0 + x, y0 - y))
        points.append((x0 - x, y0 - y))
        points.append((x0 + y, y0 + x))
        points.append((x0 - y, y0 + x))
        points.append((x0 + y, y0 - x))
        points.append((x0 - y, y0 - x))
    return points

#http://www.roguebasin.com/index.php/Bresenham%27s_Line_Algorithm
def bresenham(x1, y1, x2, y2):
    """Bresenham's Line Algorithm
        Produces a list of tuples from start and end

        >>> points1 = get_line((0, 0), (3, 4))
        >>> points2 = get_line((3, 4), (0, 0))
        >>> assert(set(points1) == set(points2))
        >>> print points1
        [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
        >>> print points2
        [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        """
    # Setup initial conditions
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

#Max distance = inf
def brezenham_to_dist(points, pose):
    for point in points:
        x = point[0]
        y = point[1]
        if map[y][x] == 0:
            return (distance(x, y, pose[0], pose[1]), False, (x,y))
    return (9999, True, points[len(points)-1])

def getViewCords(pose):
    angle1 = pose[2] - sensor_fov / 2
    angle2 = pose[2] + sensor_fov / 2
    #Scan a circle
    seach_points = circle(pose[0], pose[1], 126)
    #point3 = [sensor_range*math.cos(angle2+pose[0]), sensor_range*math.sin(angle2)+pose[1]]
    #Get raycast to this line
    found_map = []
    i = 0
    for point in seach_points:
        # Line from robot to point
        val = brezenham_to_dist(bresenham(pose[0], pose[1], point[0], point[1]), pose)
        #Is infinite for now dont include (While testing)
        if val[0] == 9999:
            pass
        else:
            angle = 2*math.pi/716*i
            found_map.append(val)
        i += 1
    print(found_map)
    points = []
    for found in found_map:
        points.append(found[2])
    #print(points)
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    return points, seach_points
    # plt.scatter(x,y)
    # plt.show()

# def getViewFromPose(pose, map):
#     return DrawFilledTriangle()

def getPoses(n):
    poses = []
    for i in range(0, n):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        angle = random.uniform(angle_range[0], angle_range[1])
        pose = [x, y, angle]
    return poses

m = 1
M = 10
for m in range(0, M):
    #Generate particles (Random poses)
    poses = getPoses(100)
    # for pose in poses:
    #     getViewFromPose(pose, raster_file)

x = 100+int(offset/2)
y = 270+int(offset/4)
point_grid, search_grid = getViewCords((x,y,math.pi/4))
for point in point_grid:
    map[point[1]][point[0]] = 100
for point in search_grid:
    map[point[1]][point[0]] = 60
map[y][x] = 150
# plt.imshow(map)
# #plt.gray()
# plt.show()

probability_grid = []
pose_similarities = []
for i in range(0, (offset*2)**2):
    probability_grid.append(0)
#Generate pose probabilitiy distrobution
#pose_sim[1] is location pose_sim[0][0] is similarity
pose_similarities.append((20,(10,6)))
pose_similarities.append((80,(10,6)))
pose_similarities.append((10,(7,7)))
pose_similarities.append((99,(5,5)))

width = offset
for pose_sim in pose_similarities:
    x = pose_sim[1][0]
    y = pose_sim[1][1]
    #index 1d array as 2d
    if probability_grid[offset * y + x] < pose_sim[0]:
        probability_grid[offset * y + x] = pose_sim[0]
indexes = []
for i in range(0, len(probability_grid)):
    indexes.append(i)

#https://stackoverflow.com/questions/2151084/map-a-2d-array-onto-a-1d-array
def setElement(arr, row,  col, value):
    arr[width * row + col] = value

def getElement(arr, row, col):
    return arr[width * row + col]

#Apply Gaussian blur so not all poses are in the exact same spot
#Array out of bounds if used near map edges
blurred_grid = probability_grid
for i in range(offset):
    for j in range(offset):
        val = getElement(probability_grid, j, i)
        if val > 1:
            #print(val)
            setElement(blurred_grid, j, i, val*4/16)
            setElement(blurred_grid, j + 1, i + 1, val/ 16)
            setElement(blurred_grid, j, i + 1, val * 2 / 16)
            setElement(blurred_grid, j - 1, i + 1, val / 16)
            setElement(blurred_grid, j - 1, i, val * 2/ 16)
            setElement(blurred_grid, j - 1, i -1, val / 16)
            setElement(blurred_grid, j, i - 1, val * 2 / 16)
            setElement(blurred_grid, j-1, i-1, val / 16)
            setElement(blurred_grid, j - 1, i, val * 2/ 16)

probability_grid = blurred_grid

#Generate new poses
for i in range(0,100):
    index = random.choices(indexes, weights=probability_grid)
    y = int(index[0]/300)
    x = index[0]%300
    assert getElement(probability_grid, y, x) - probability_grid[index[0]] == 0

test_blur = []
for i in range(0, offset*2):
    test_blur.append([])
    for j in range(0, offset*2):
        val = getElement(probability_grid, j, i)
        if val > 1:
            print(val)
        test_blur[i].append(val)

plt.imshow(test_blur)
plt.gray()
plt.show()
