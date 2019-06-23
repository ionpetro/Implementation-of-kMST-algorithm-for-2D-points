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

def subSquares(diameter, rootSquare, k, angle):
    '''
    This method is supposed to devide the rootSquare into
    k subsquares with side = diameter/root(k)
    '''
    side = diameter/math.sqrt(k)
    diagonial_length = math.sqrt(side ** 2 + side ** 2)
    subAngle = angle + 45
    subSquares = {}
    x1 = rootSquare['b'][0]
    y1 = rootSquare['b'][1] 
    # TODO: It seems that I don't need to have the top right coordinate from the squareRoot
    # TODO: Or I have done a mistake!

    # x2 = rootSquare['t'][0]
    # y2 = rootSquare['t'][1]
    starting_x = x1
    starting_y = y1
    save_x, save_y = starting_x, starting_y
    # I am having check number of squares per line in my shape
    check = int(math.sqrt(k))
    for i in range(1, k+1):
        dic = {}
        dic['b'] = [starting_x, starting_y]
        dic['t'] = [diagonial_length * math.cos(math.radians(subAngle)) + starting_x, diagonial_length * math.sin(math.radians(subAngle)) + starting_y]
        subSquares[i] = dic
        # the point of this if statement is to divide the rootSquare
        # into k squares where horizontal and vertical squares add up to k
        # so each line will contain root(k) squares and then I will change the line
        if i % check == 0:
            # change line (check the y coordinate)
            # adding 90 degrees to the angle because I want to move to the y axis
            next_starting_x = side * math.cos(math.radians(angle + 90)) + save_x
            next_starting_y = side * math.sin(math.radians(angle + 90)) + save_y 
            starting_x, starting_y = next_starting_x, next_starting_y
            save_x, save_y = starting_x, starting_y
            # print("I got in if")
        else:
            next_starting_x = side * math.cos(math.radians(angle)) + starting_x
            next_starting_y = side * math.sin(math.radians(angle)) + starting_y 
            starting_x, starting_y = next_starting_x, next_starting_y
            # print("I got in else")
            # keep with the same y and change x
    print("subSquares", subSquares)
    return subSquares

def checkforPoints(subSq, point):
    pointsPerSquare = {}
    pickedPoints = {}
    for key in subSq:
        x1 = subSq[key]['b'][0]
        y1 = subSq[key]['b'][1]
        x2 = subSq[key]['t'][0]
        y2 = subSq[key]['t'][1]
        count = 0
        points = []
        for p in point:
            x = p[0]
            y = p[1]
            # TODO: this does not work with rotated squares
            if (x >= x1 and x <= x2 and y >= y1 and y <= y2): 
                # This means that the point is inside the square
                count += 1
                points.append(p)
                # print("the point", p, "is inside the square", subSq[key])
            pickedPoints[key] = points  
            pointsPerSquare[key] = count
    return pointsPerSquare, pickedPoints


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
            subSq = subSquares(diameter, rootSquare, k, angle)
            pointsPerSquare, pickedPoints = checkforPoints(subSq, point)
            print(pointsPerSquare, pickedPoints)
            sortedpointsPerSquare = sorted(pointsPerSquare, key=pointsPerSquare.get, reverse= True)
            print("These are the sorted ones", sortedpointsPerSquare)
            pointCount = 0
            i = 0
            try:       
                while pointCount < k:
                    pointCount += pointsPerSquare[sortedpointsPerSquare[i]]    
                    i += 1
            except IndexError:
                print("There are not enough points to the Square!")
            print("__________________\n")
            # print("the side is:", side)
            # print("the radius is: ", radius)
        # A = (π/4) × D^2
        # circle_area = (math.pi/4) * diameter
        
k = 4
kMST(point, k)
