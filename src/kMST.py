import pprint

input_file = '../tests/points.txt'
# Text format
# 4.43 4.55
# 6.43 3.22

# read the points of the file and save them on a set
def read_file(input_file):
    lines = set()
    with open(input_file) as input_file:
        for line in input_file:
            x, y = line.split()
            lines.add((float(x),float(y)))
        return lines

# save the set of points on a variable
point = read_file(input_file)

def kMST(point):
    for points in point:
        print(points)

kMST(point)