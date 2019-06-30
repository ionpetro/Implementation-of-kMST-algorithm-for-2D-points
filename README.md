# Implementation-of-kMST-algorithm-for-points-on-the-plane

This is an algorithm which is about **Finding the minimum spanning tree constructed by k nodes**. Is written in **Python 3.X** and is based on Ravi, R., Sundaram, R., Marathe, M. V., Rosenkrantz, D. J., & Ravi, S. S. (1996). Spanning trees—short or small. SIAM Journal on Discrete Mathematics, 9(2), 178-200.

You can find the **paper** on the Cornell University [arXin.org](https://arxiv.org/) papers archiv [here](https://arxiv.org/abs/math/9409222).

This work was given as a bonus project from [Panos Louridas](https://github.com/louridas) in course **Algorithms and Data Structures** during by studies on *Department of Management Science and Technology*, Athens University of Economics and Business [(aueb)](www.aueb.gr).

## Prerequesities

Install the following libraries:

```
pip install math, argparse, numpy, scipy
```

## Getting Started

Download the repo and move to src file;

```
git clone https://github.com/ionpetro/Implementation-of-kMST-algorithm-for-2D-points.git

cd src/
```

Run the program:

```
python kMst.py k input_file
```
Arguments:

```
positional arguments:
  k           Enter the k value
  input_file  Please insert an input txt file with points
```

**Example:** For the file [points.txt](tests/points.txt)

```
python kMST.py 4 ../test/points.txt
```

Result:
```
This is the kMST result: 
9.571067811865476
```

## Acknowledgements

* The Minimum Spanning tree was implemented using the Prim's algorithm using [Kruskal algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm) with the **scipy sparse csgraph** library, you can find it here: [link](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.minimum_spanning_tree.html#scipy.sparse.csgraph.minimum_spanning_tree)

* The Heron's implementation for checking if a point in inside a square or not, was based to a stack exchange post where you can find here: [link](https://math.stackexchange.com/q/190403)
