import pprint
import math
import argparse
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

__author_ = "Ion Petropoulos"

parser = argparse.ArgumentParser()
parser.add_argument("k", help="Enter the k value")
parser.add_argument("input_file", help="Please insert an input json file")
args = parser.parse_args()

input_file = args.input_file
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
    return subSquares

def checkforPoints(subSq, point, side, angle):
    pointsPerSquare = {}
    pickedPoints = {}
    for key in subSq:
        x1 = subSq[key]['b'][0]
        y1 = subSq[key]['b'][1]
        x2 = subSq[key]['t'][0]
        y2 = subSq[key]['t'][1]
        # Here i need to calculate the x3,y3 and x4,y4
        # for the rotated squares
        x3 = x1 + side * math.cos(math.radians(angle + 90)) #top left coordinate
        y3 = y1 + side * math.sin(math.radians(angle + 90)) #top left coordinate
        x4 = x2 + side * math.cos(math.radians(angle - 90)) #bottom right coordinate
        y4 = y2 + side * math.sin(math.radians(angle - 90)) #botom right coordinate
        count = 0
        points = []
        for p in point:
            x = p[0]
            y = p[1]
            #square sides
            a1 = math.sqrt((x2-x3)**2 + (y2-y3)**2)
            a2 = math.sqrt((x2-x4)**2 + (y2-y4)**2)
            a3 = math.sqrt((x3-x1)**2 + (y3-y1)**2)
            a4 = math.sqrt((x4-x1)**2 + (y4-y1)**2)
            # The area of the squale
            A = a1 * a2
            # Calculate the length of the line segments
            b1 = math.sqrt((x1-x)**2 + (y1-y)**2)
            b2 = math.sqrt((x2-x)**2 + (y2-y)**2)
            b3 = math.sqrt((x3-x)**2 + (y3-y)**2)
            b4 = math.sqrt((x4-x)**2 + (y4-y)**2)
            # calculate the areas of the Triangls using Heron's formula
            u1 = (a1 + b2 + b3)/2
            u2 = (a2 + b2 + b4)/2
            u3 = (a3 + b1 + b3)/2
            u4 = (a4 + b1 + b4)/2
            try:
                A1 = math.sqrt(u1*(u1-a1)*(u1-b2)*(u1-b3))
                A2 = math.sqrt(u2*(u2-a2)*(u2-b2)*(u2-b4))
                A3 = math.sqrt(u3*(u3-a3)*(u3-b1)*(u3-b3))
                A4 = math.sqrt(u4*(u4-a4)*(u4-b1)*(u4-b4))
            except ValueError:
                print("Bug on the Heron's formula implementation")
            triangleArea = (A1 + A2 + A3 + A4)
            # Accurancy up to 2 decimals
            if round(A, 2) == round(triangleArea, 2):
                # This means that the point is inside the square
                count += 1
                points.append(p)
                # print("This one got in")
                # print("the point", p, "is inside the square", subSq[key])
            else:
                # print("The point", p, "is not inside the square!!")
                # The point is not inside the square
                # print(p ,"failed because", A, "not equal to", (A1 + A2 + A3 + A4))
                pass
        pickedPoints[key] = points  
        pointsPerSquare[key] = count
    return pointsPerSquare, pickedPoints

def chooseSells(sortedpointsPerSquare, pickedPoints, k):
    count = 0
    i = 0
    selectedSquares = []
    try:
        while count < k:
                
            indexofpoints = sortedpointsPerSquare[i]
            points = pickedPoints[indexofpoints]
            for j in range(len(points)):
                # check for duplicate values 
                if points[j] not in selectedSquares:
                    selectedSquares.append(points[j])
                else:
                    count -= 1
            count += len(points)
            i += 1
            # this if statement discard the last N iteams
            # from a list if it exceeds the number k
            # not tested code
            if count > k:
                difference = count - k
                del selectedSquares[-difference:]
    except IndexError as e:
        print("Not enought k values were collected!")
        print("Error type: ")
        print(e)
        quit()
    return selectedSquares
    # print("megethos", len(selectedSquares))
    # print("selectedSquares", selectedSquares)


def kMST(point, k):
    # print(point)
    results = []
    list_of_pairs = create_pairs(point)
    for pair in list_of_pairs:
        x1 = pair[0][0]
        x2 = pair[1][0]
        y1 = pair[0][1]
        y2 = pair[1][1]
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
            # create circumscribing square
            # print("I'm here with subset", subS)
            edgep = edgepair(pair, diameter, distance, angle)
            # print("this is the edgesquare")
            # pprint.pprint(edgep)
            rootSquare = square(radius, edgep, angle)
            # This is the subsquare side (d/root(k))
            subSq = subSquares(diameter, rootSquare, k, angle)
            side = diameter/math.sqrt(k)
            pointsPerSquare, pickedPoints = checkforPoints(subSq, point, side, angle)
            sortedpointsPerSquare = sorted(pointsPerSquare, key=pointsPerSquare.get, reverse= True)
            # print("These are the sorted ones", sortedpointsPerSquare)
            # #Error handling when sortedpointsPerSquare list is out of range
            # try:       
            #     while pointCount < k:
            #         pointCount += pointsPerSquare[sortedpointsPerSquare[i]]    
            #         i += 1
            # except IndexError:
            #     print("Something is wrong here!")
            # print("__________________\n")
            selectedSquares = chooseSells(sortedpointsPerSquare, pickedPoints, k)
            l = len(selectedSquares)
            # zeros = np.zeros((l,l))
            matrix = []
            for i in range(l):
                innerlist = []
                for j in range(l):
                    innerlist.append(math.hypot(selectedSquares[j][0] - selectedSquares[i][0], \
                        selectedSquares[j][1] - selectedSquares[i][1]))
                matrix.append(innerlist)

            x = np.array(matrix)
            x.reshape(l,l)
            tcsr = minimum_spanning_tree(x)
            tcsr.toarray().astype(float) 
            results.append(tcsr.sum())

    try:
        x = min(results)
    except ValueError:
        print("Algorithm prerequisities have not been met!")
        print("Maybe k value is set too high")
        quit()        
    return x
    

            # print("the side is:", side)
            # print("the radius is: ", radius)
        # A = (π/4) × D^2
        # circle_area = (math.pi/4) * diameter
     
print("This is the kMST result: ")
k = int(args.k)
print(kMST(point, k))
