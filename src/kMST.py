import pprint
import math

input_file = '../tests/points.txt'
# Text format
# 4.43 4.55
# 6.43 3.22

# read the points of the file and save them on a set
def read_file(input_file):
    lines = []
    with open(input_file) as input_file:
        for line in input_file:
            x, y = line.split()
            lines.append([float(x),float(y)])
        return lines

# save the set of points on a variable
point = read_file(input_file)

def create_pairs(point):
    list_of_pairs = []
    for p1 in range(len(point)):
        for p2 in range(p1 + 1, len(point)):
            list_of_pairs.append([point[p1], point[p2]])
    return list_of_pairs

def find_center(x1, x2, y1, y2):
    x_m_point = (x1 + x2)/2
    y_m_point = (y1 + y2)/2
    return x_m_point, y_m_point

def checkSubset(subS, k):
    if len(subS) >= k:
        return True
    return False

def square(radius, mid_x, mid_y):
    squareDic = {}
    tr, tl, br, bl = 0, 0, 0, 0
    #top right coordinate
    squareDic[tr] = (mid_x + radius, mid_y - radius)
    # top left coordinate
    squareDic[tl] = (mid_x + radius, mid_y + radius)   
    # bottom right coordinate
    squareDic[br] = (mid_x + radius, mid_y + radius)
    # bottom left coordinate
    squareDic[bl] = (mid_x + radius, mid_y + radius)
    return squareDic


def kMST(point, k):
    print(point)
    list_of_pairs = create_pairs(point)
    for pair in list_of_pairs:
        x1 = pair[0][0]
        x2 = pair[1][0]
        y1 = pair[0][1]
        y2 = pair[1][1]
        slope = (y1 - y2)/(x1 - x2)
        distance = math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        # let's say we choose the first point
        print("line: y - " + str(y1) + " = " + str(slope) + "(x-" + str(x1) +")") 
        diameter =  math.sqrt(3)*distance
        radius = diameter/2
        mid_x, mid_y = find_center(x1, x2, y1, y2)
        subS = []
        for p in point:
            if point == [x1, y1] or point == [x2, y2]:
                # It's the same point
                continue
            else:
                # check if the point is inside the circle
                x = p[0]
                y = p[1]
                if ((x - mid_x)**2 + (y - mid_y)**2) < radius**2:
                    subS.append([x, y])
                else:
                    print(False)
        if not checkSubset(subS, k):
            # The subSet contains fewer than k points
            continue
        else:
            squareDic = {}
            squareDic = square(radius, mid_x, mid_y)
        # A = (π/4) × D^2
        # circle_area = (math.pi/4) * diameter
        
k = 2
kMST(point, k)