import random
import time

import numpy as np
from tree import Tree
import quads
import gaphas.quadtree
import pyqtree
import matplotlib.pyplot as plt

INSERTION_BENCHMARKING_TIME = 10  # How many seconds to insert items for each algorithm
INSERTION_MEASUREMENTS = 100

INTERSECT_ITEMS = 100000
INTERSECT_MEASUREMENTS = 50
INTERSECT_MEASURE_TIME = 0.2


class PyQtreeWrapper:
    def __init__(self):
        self.tree = pyqtree.Index(bbox=(0, 0, 1, 1))
        self.name = "pyqtree"

    def insert(self, item, pos):
        self.tree.insert((item, pos), bbox=(*pos, pos[0], pos[1])),

    def intersect(self, pos, r):
        return [x for x in self.tree.intersect(np.concatenate([pos - r, pos + r]))]


class TreeWrapper:
    def __init__(self):
        self.tree = Tree((0, 0, 1, 1))
        self.name = "tree"

    def insert(self, item, pos):
        self.tree.insert((item, pos), [*pos, *pos])

    def intersect(self, pos, r):
        return [x for x in self.tree.intersect([*(pos - r), *(pos + r)])]


class GaphasWrapper:
    def __init__(self):
        self.tree = gaphas.quadtree.Quadtree()
        self.name = "gaphas"

    def insert(self, item, pos):
        self.tree.add((item, pos), [*pos, 0, 0]),

    def intersect(self, pos, r):
        return [x for x in self.tree.find_intersect(np.concatenate([pos - r, pos - pos + r + r]))]


class QuadsWrapper:
    def __init__(self):
        self.tree = quads.QuadTree((0.5, 0.5), 1, 1)
        self.name = "quads"

    def insert(self, item, pos):
        self.tree.insert(pos, data=(item, pos)),

    def intersect(self, pos, r):
        return [x.data for x in self.tree.within_bb(quads.BoundingBox(*(pos - r), *(pos + r)))]


def insertion_test():
    methods = [
        PyQtreeWrapper(),
        TreeWrapper(),
        QuadsWrapper(),
        GaphasWrapper(),
    ]

    insertions_between_each_check = 100
    time_between_each_measure = INSERTION_BENCHMARKING_TIME / INSERTION_MEASUREMENTS
    plt.figure(0)

    for method in methods:
        random.seed(1234)
        print(f"Benchmarking insertion for {method.name}.")
        start_time = time.time()
        measure = 1
        count = 0
        X = []
        Y = []
        while measure <= INSERTION_MEASUREMENTS:
            for i in range(insertions_between_each_check):
                x = (random.random())
                y = (random.random())
                method.insert(count, (x, y))
                count += 1
            current_time = time.time()
            if current_time - start_time > time_between_each_measure * measure:
                X.append(current_time-start_time)
                Y.append(count)
                measure += 1
        plt.plot(X, Y)
    plt.legend([x.name for x in methods])
    plt.xlabel("Seconds")
    plt.ylabel("Insertions")


def intersect_test():
    methods = [
        PyQtreeWrapper(),
        TreeWrapper(),
        QuadsWrapper(),
        GaphasWrapper(),
    ]

    random.seed(1234)
    for i in range(INTERSECT_ITEMS):
        x = (random.random())
        y = (random.random())
        for method in methods:
            method.insert(i, (x, y))
    plt.figure(1)

    center = np.array([.5, .5])
    num_items_found = {}
    for method in methods:
        print(f"Benchmarking intersection for {method.name}...")
        radius = []
        framerate = []
        items_found = []
        for i in range(1, INTERSECT_MEASUREMENTS + 1):
            r = i / INTERSECT_MEASUREMENTS
            count = 0
            start_time = time.time()
            while time.time() - start_time < INTERSECT_MEASURE_TIME:
                count += 1
                items = method.intersect(center, r / 2)
                if count == 1:
                    items_found.append(len(items))
            framerate.append(count/(time.time()-start_time))
            radius.append(r)
        num_items_found[method.name] = items_found
        plt.plot(radius, framerate)
    plt.legend([x.name for x in methods])
    plt.xlabel("Query region size")
    plt.ylabel("Framerate")


def main():
    """Benchmarking of own implementation and three different libraries.

    The benchmarking will compare the duration of inserting objects as well as framerate
    of querying all objects within a region."""

    print("Benchmarking insertion")
    insertion_test()
    print("Benchmarking intersection")
    intersect_test()
    plt.show()


if __name__ == "__main__":
    main()
