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

def square(radius, mid_x, mid_y):
    rootSquare = {}
    '''We are going to represent a square by using only the
    top right and the bottom left coordinates since all of
    the square's sides are equal
    '''
    #top right coordinate
    rootSquare['tr'] = (mid_x + radius, mid_y + radius)
    # bottom left coordinate
    rootSquare['bl'] = (mid_x - radius, mid_y - radius)
    return rootSquare

def numberofSquares(diameter, side):
    if diameter % side > 0:
        numberofSquares = ((diameter // side) + 1) ** 2
    else:
        numberofSquares = (diameter // side) ** 2
    return numberofSquares

def subSquares(diameter, side, rootSquare):
    #calculate the number of squares
    subSquares = {}
    sqNum = numberofSquares(diameter, side)
    count = 0
    x1 = rootSquare['bl'][0]
    save = x1
    x2 = rootSquare['bl'][1]
    y1 = rootSquare['tr'][0]
    y2 = rootSquare['tr'][1]
    print(int(sqNum))
    for _ in range(int(sqNum)//2):
        dic = {}
        for _ in range(int(sqNum)//2):
            dic['bl'] = [x1,y1]
            dic['tr'] = [x1+side,y1+side]
            # here I am not taking angle into consideration
            # i should calculate angle of the square in reference with
            # a 0 degree line 
            subSquares[count] = dic
            x1 = x1+side
        x1 = save
        y1 = y1 + side
    return subSquares


def kMST(point, k):
    # print(point)
    list_of_pairs = create_pairs(point)
    for pair in list_of_pairs:
        x1 = pair[0][0]
        x2 = pair[1][0]
        y1 = pair[0][1]
        y2 = pair[1][1]
        print(pair)
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
            print("pair", pair, "failed!!")
            continue
        else:
            # create circumscribing square
            print("I'm here with subset", subS)
            rootSquare = square(radius, mid_x, mid_y)
            print("this is the squareDic")
            pprint.pprint(rootSquare)
            side = diameter/math.sqrt(k)
            x = subSquares(diameter, side, rootSquare)
            print("subsquares", x)
            print("__________________\n")
            # print("the side is:", side)
            # print("the radius is: ", radius)
        # A = (π/4) × D^2
        # circle_area = (math.pi/4) * diameter
        
k = 4
kMST(point, k)