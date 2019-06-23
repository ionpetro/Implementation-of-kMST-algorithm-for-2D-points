import pprint
import math

input_file = '../tests/points1.txt'
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
    # print("The subset is", subS)
    if len(subS) >= k:
        return True
    return False

def edgepair(pair, diameter, distance, angle):
    edgepair = []
    distance_to_edge = (diameter - distance) / 2
    # print("this is the distance to edge", distance_to_edge)
    x1 = pair[0][0] - math.cos(math.radians(angle)) * distance_to_edge
    x2 = pair[1][0] + math.cos(math.radians(angle)) * distance_to_edge
    y1 = pair[0][1] - math.sin(math.radians(angle)) * distance_to_edge
    y2 = pair[1][1] + math.sin(math.radians(angle)) * distance_to_edge
    edgepair = [[x1,y1], [x2,y2]]
    return edgepair

def square(radius, edgepair, angle):
    rootSquare = {}
    x1 = edgepair[0][0]
    x2 = edgepair[1][0]
    y1 = edgepair[0][1]
    y2 = edgepair[1][1]
    # print("this is the angle", angle)
    bottom_angle = -90 + angle
    top_angle = 90 + angle
    
    # bottom left coordinate
    rootSquare['b'] = (radius * math.cos(math.radians(bottom_angle)) + x1, \
         radius * math.sin(math.radians(bottom_angle)) + y1)
    #top right coordinate
    rootSquare['t'] = (radius * math.cos(math.radians(top_angle)) + x2,\
         radius * math.sin(math.radians(top_angle)) + y2)
    return rootSquare

# I don't need to calculate the numberofSquare because 
# I should devide the rootSquare into k squares

# def numberofSquares(diameter, side):
#     if diameter % side > 0:
#         numberofSquares = ((diameter // side) + 1) ** 2
#     else:
#         numberofSquares = (diameter // side) ** 2
#     return numberofSquares

def subSquares(diameter, rootSquare, k, angle):
    '''
    This method is supposed to devide the rootSquare into
    k subsquares with side = dimaeter/root(k)
    '''
    side = diameter/math.sqrt(k)
    subSquares = {}
    x1 = rootSquare['b'][0]
    x2 = rootSquare['b'][1] 
    y1 = rootSquare['t'][0]
    y2 = rootSquare['t'][1]
    # how do I cover the hole rootSquare?
    return


def kMST(point, k):
    # print(point)
    list_of_pairs = create_pairs(point)
    for pair in list_of_pairs:
        x1 = pair[0][0]
        x2 = pair[1][0]
        y1 = pair[0][1]
        y2 = pair[1][1]
        print("pair", pair)
        # slope = (y1 - y2)/(x1 - x2)
        distance = math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        # let's say we choose the first point
        # print("line: y - " + str(y1) + " = " + str(slope) + "(x-" + str(x1) +")") 
        diameter =  math.sqrt(3)*distance
        # print(diameter)
        radius = diameter/2
        # print(radius)
        mid_x, mid_y = find_center(x1, x2, y1, y2)
        # print(mid_x)
        # print(mid_y)
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
        if not checkSubset(subS, k):
            # The subSet contains fewer than k points
            # print("pair", pair, "failed!!")
            continue
        else:
            # here I calculate the entry angle
            angle = math.degrees(math.atan2(y2-y1,x2-x1))
            print("This is the angle", angle)
            # create circumscribing square
            # print("I'm here with subset", subS)
            edgep = edgepair(pair, diameter, distance, angle)
            # print("this is the edgesquare")
            # pprint.pprint(edgep)
            rootSquare = square(radius, edgep, angle)
            print("this is the rootSquare")
            pprint.pprint(rootSquare)
            # This is the subsquare side (d/root(k))
            x = subSquares(diameter, rootSquare, k, angle)
            # print("subsquares", x)
            print("__________________\n")
            # print("the side is:", side)
            # print("the radius is: ", radius)
        # A = (π/4) × D^2
        # circle_area = (math.pi/4) * diameter
        
k = 3
kMST(point, k)
