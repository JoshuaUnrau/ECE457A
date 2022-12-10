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
def grid_bounds(geom, delta):
    minx, miny, maxx, maxy = geom.bounds
    nx = int(maxx - minx + 1)
    ny = int(maxy - miny + 1)
    print(nx)
    gx, gy = np.linspace(minx,maxx,nx), np.linspace(miny,maxy,ny)
    print(gx)
    grid = []
    for i in range(len(gx)-1):
        for j in range(len(gy)-1):
            poly_ij = Polygon([[gx[i],gy[j]],[gx[i],gy[j+1]],[gx[i+1],gy[j+1]],[gx[i+1],gy[j]]])
            grid.append(poly_ij)
            #grid.append((i,j))
    return grid

def partition(geom, delta):
    prepared_geom = prep(geom)
    grid = list(filter(prepared_geom.intersects, grid_bounds(geom, delta)))
    #grid = grid_bounds(geom, delta)
    return grid

#geom = Polygon([[0,0],[5,-5],[5,5],[0,0]])
geom = Polygon([[30,60],[60,75],[60,50],[30,60]])
grid = partition(geom, 1)

point_grid = []
for poly in grid:
    #continue
    #print(list(poly.exterior.coords)[0])
    point = list(poly.exterior.coords)[0]
    point_grid.append((int(point[0]),int(point[1])))

#https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
def line_intersection(line1, line2):
    intersection = True
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        intersection = False
        return 0, 0, intersection
       #raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    intersection = True
    return x, y, intersection


def getViewCords(pose):
    angle1 = pose[2] - sensor_fov / 2
    angle2 = pose[2] + sensor_fov / 2
    # Scan a arc
    # point1 = [sensor_range*math.cos(angle1)+pose[0], sensor_range*math.sin(angle1)+pose[1]]
    # point2 = [sensor_range*math.cos(angle2)+pose[0], sensor_range*math.sin(angle2)+pose[1]]
    # Scan a Square
    # point1 = [-sensor_range + pose[0], sensor_range + pose[1]]
    # point2 = [sensor_range + pose[0], sensor_range + pose[1]]
    # point3 = [sensor_range + pose[0], -sensor_range + pose[1]]
    # point4 = [-sensor_range + pose[0], -sensor_range + pose[1]]
    # seach_points = []
    # seach_points.extend(bresenham(point1[0], point1[1], point2[0], point2[1]))
    # seach_points.extend(bresenham(point2[0], point2[1], point3[0], point3[1]))
    # seach_points.extend(bresenham(point3[0], point3[1], point4[0], point4[1]))
    # seach_points.extend(bresenham(point1[0], point1[1], point4[0], point4[1]))

    # Scan a circle
    seach_points = circle(0, 0, 126)
    # point3 = [sensor_range*math.cos(angle2+pose[0]), sensor_range*math.sin(angle2)+pose[1]]
    # Get raycast to this line
    print(point1)
    print(point2)
    found_map = []
    for point in seach_points:
        # Line from robot to point
        val = brezenham_to_dist(bresenham(pose[0], pose[1], point[0], point[1]), pose)
        # Is infinite for now dont include
        if val[0] == 9999:
            pass
        else:
            found_map.append(val)
    print(found_map)
    points = []
    for found in found_map:
        points.append(found[1])
    # print(points)
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    return points, seach_points
    # plt.scatter(x,y)
    # plt.show()

def update_pose_distribution(self, pose_dist):
        self.probability_grid = []
        pose_similarities = pose_dist
        for i in range(0, (self.offset * 2) ** 2):
            self.probability_grid.append(0)
        #Generate pose probabilitiy distrobution
        #pose_sim[1] is location pose_sim[0][0] is similarity
        width = self.offset
        for pose_sim in pose_similarities:
            x = pose_sim[1][0]
            y = pose_sim[1][1]
            # index 1d array as 2d
            if self.getElement(self.probability_grid, y, x) < pose_sim[0]:
                self.setElement(self.probability_grid, y, x, pose_sim[0])

        # Apply Gaussian blur so not all poses are in the exact same spot
        # Array out of bounds if used near map edges
        blurred_grid = self.probability_grid.copy()
        for i in range(self.offset * 2):
            for j in range(self.offset * 2):
                val = self.getElement(self.probability_grid, j, i)
                if val > 1:
                    # print(val)
                    self.setElement(blurred_grid, j, i, val * 4 / 16)
                    self.setElement(blurred_grid, j + 1, i + 1, val / 16)
                    self.setElement(blurred_grid, j, i + 1, val * 2 / 16)
                    self.setElement(blurred_grid, j - 1, i + 1, val / 16)
                    self.setElement(blurred_grid, j - 1, i, val * 2 / 16)
                    self.setElement(blurred_grid, j + 1, i - 1, val / 16)
                    self.setElement(blurred_grid, j, i - 1, val * 2 / 16)
                    self.setElement(blurred_grid, j - 1, i - 1, val / 16)
                    self.setElement(blurred_grid, j + 1, i, val * 2 / 16)

        self.probability_grid = blurred_grid

        #For testing
        test_blur = []
        for i in range(0, self.offset * 2):
            test_blur.append([])
            for j in range(0, self.offset * 2):
                val = self.getElement(self.probability_grid, j, i)
                if val > 1:
                    pass
                    #print(val)
                test_blur[i].append(val)
        #print("Testing blur")
        # plt.imshow(test_blur)
        # plt.gray()
        # plt.show()
        # quit()