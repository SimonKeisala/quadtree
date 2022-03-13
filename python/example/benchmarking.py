import random
import time

import numpy as np
import pygame
import tree
import quads
import gaphas.quadtree
import pyqtree

RADIUS = 20


def main():
    items = []
    random.seed(1234)
    gaphas_tree = gaphas.quadtree.Quadtree()
    quads_tree = quads.QuadTree((256, 256), 512, 512)
    pyqtree_tree = pyqtree.Index(bbox=(0, 0, 512, 512))
    tree_tree = tree.Tree((256, 256), 512)
    for i in range(100000):
        x = (random.random()) * 512
        y = (random.random()) * 512
        items.append((i, (x, y)))

    start = time.time()
    for i, pt in items:
        gaphas_tree.add((i, pt), (*pt, 1, 1))
    gaphas_time = time.time() - start
    print(f"gaphas_time: {gaphas_time:.2f}")
    start = time.time()
    for i, pt in items:
        quads_tree.insert(pt, data=(i, pt))
    quads_time = time.time() - start
    print(f"quads_time: {quads_time:.2f}")
    start = time.time()
    for i, (x, y) in items:
        pyqtree_tree.insert((i, (x, y)),
                            bbox=(x, y, x, y))
    pyqtree_time = time.time() - start
    print(f"pyqtree_time: {pyqtree_time:.2f}")
    start = time.time()
    for i, pt in items:
        tree_tree.insert((i, pt), pt)
    tree_time = time.time() - start
    print(f"tree_time: {tree_time:.2f}")

    intersects = {
        "pyqtree_tree": lambda pos, r: pyqtree_tree.intersect(np.concatenate([pos-r, pos+r])),
        "tree_tree": lambda pos, r: tree_tree.intersect(pos, r),
        "gaphas_tree": lambda pos, r: gaphas_tree.find_intersect(np.concatenate([pos-r, pos-pos+r+r])),
        "quads_tree": lambda pos, r: quads_tree.within_bb(quads.BoundingBox(*(pos-r), *(pos+r)))
    }
    extract = {
        "pyqtree_tree": lambda data: data,
        "tree_tree": lambda data: data,
        "gaphas_tree": lambda data: data,
        "quads_tree": lambda data: data.data,
    }


    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    running = True
    frames = 0
    last_measure = time.time()
    mouse_pos = np.zeros(2)
    r_squared = RADIUS * RADIUS
    methods = [x for x in intersects]
    method_idx = 0
    items_found = 0
    while running:
        frames += 1
        if time.time() - last_measure > 1:
            last_measure += 1
            print(f"{methods[method_idx]}:{frames}")
            print(f"items found: {items_found}\n")

            frames = 0
            method_idx = (method_idx+1) % len(methods)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = np.array(event.pos)

        #mouse_pos = np.array([256, 256])
        screen.fill((255, 255, 255))
        found_items = [x for x in intersects[methods[method_idx]](mouse_pos, RADIUS)]
        items_found = len(found_items)
        for item in found_items:
            data = extract[methods[method_idx]](item)
            pygame.draw.circle(screen, (255, 0, 0), data[1], 1)
        #for item, point in items:
        #    if np.sum((mouse_pos - point) ** 2) < r_squared:
        #        pygame.draw.circle(screen, (255, 0, 0), point, 1)

        pygame.display.flip()


if __name__ == "__main__":
    main()
