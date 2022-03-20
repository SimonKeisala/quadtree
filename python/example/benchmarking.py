import random
import time

import numpy as np
import tree
import quads
import gaphas.quadtree
import pyqtree
import matplotlib.pyplot as plt


def main():
    """Benchmarking of own implementation and three different libraries.

    The benchmarking will compare the duration of inserting objects as well as framerate
    of querying all objects within a region."""

    # Create the sample points to use for all libraries
    items = []
    random.seed(1234)
    for i in range(100000):
        x = (random.random()) * 500
        y = (random.random()) * 500
        items.append((i, (x, y)))

    # Instantiate all libraries
    gaphas_tree = gaphas.quadtree.Quadtree()
    quads_tree = quads.QuadTree((250, 250), 500, 500)
    pyqtree_tree = pyqtree.Index(bbox=(0, 0, 500, 500))
    tree_quad_tree = tree.Quadtree((0, 0, 500, 500))
    tree_tree = tree.Tree((250,250), 500)

    # Map common functions for inserting, perform intersection and extracting the intersected data
    insert = {
        "pyqtree": lambda item, pos: pyqtree_tree.insert((item, pos), bbox=(*pos, pos[0], pos[1])),
        "tree_quadtree": lambda item, pos: tree_quad_tree.insert((item, pos), (*pos, pos[0], pos[1])),
        #"tree_tree": lambda item, pos: tree_tree.insert((item, pos), pos),
        "gaphas": lambda item, pos: gaphas_tree.add((item, pos), [*pos, 0, 0]),
        #"quads": lambda item, pos: quads_tree.insert(pos, data=(item, pos)),
    }
    intersect = {
        "pyqtree": lambda pos, r: pyqtree_tree.intersect(np.concatenate([pos-r, pos+r])),
        "tree_quadtree": lambda pos, r: tree_quad_tree.intersect(*(pos - r), *(pos + r)),
        #"tree_tree": lambda pos, r: tree_tree.intersect(pos, r),
        "gaphas": lambda pos, r: gaphas_tree.find_intersect(np.concatenate([pos-r, pos-pos+r+r])),
        #"quads": lambda pos, r: quads_tree.within_bb(quads.BoundingBox(*(pos-r), *(pos+r)))
    }
    extract = {
        "pyqtree": lambda data: data,
        "tree_quadtree": lambda data: data,
        #"tree_tree": lambda data: data,
        "gaphas": lambda data: data,
        #"quads": lambda data: data.data,
    }
    for method in insert:
        start = time.time()
        for i, pt in items:
            insert[method](i, pt)
        end = time.time()
        print(f"{method}: {end-start:.2f}s")

    frames = 0
    mouse_pos = np.array([250, 250])
    measure_duration = .1
    r = 2.5
    while r <= 255:
        counts = {}
        for name, method in intersect.items():
            counts[name] = len([extract[name](item) for item in intersect[name](mouse_pos, r)])
        last_value = -1
        last_key = None
        for key, value in counts.items():
            if last_key and value != last_value:
                print(f"Difference between: {last_key} and {key}: {last_value} -- {value}")
            last_key = key
            last_value = value
        r += 2.5

    for name, method in intersect.items():
        r = 2.5
        last_measure = time.time()
        radius = []
        framerate = []
        while r <= 255:
            frames += 1
            delta = time.time() - last_measure
            result = [extract[name](item) for item in intersect[name](mouse_pos, r)]
            if delta > measure_duration:
                radius.append(r)
                framerate.append(frames/delta)
                frames = 0
                r += 2.5
                last_measure += delta
        plt.plot(radius, framerate)
    plt.legend([name for name in intersect])
    plt.show()


if __name__ == "__main__":
    main()
