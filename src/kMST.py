import pprint
import itertools

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

def kMST(point):
    list_of_pairs = create_pairs(point)
    return list_of_pairs

pprint.pprint(kMST(point))