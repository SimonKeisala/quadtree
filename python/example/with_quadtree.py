import random
import time

import numpy as np
import pygame

from tree import Tree, Quadtree

RADIUS = 20


def main():
    quadtree = Quadtree((0, 0, 512, 512))
    random.seed(1234)
    start = time.time()
    for i in range(10000):
        x = (random.random()) * 512
        y = (random.random()) * 512
        quadtree.insert((i, (x, y)), (x, y, x, y))
    end = time.time()
    print(end-start)

    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    running = True
    frames = 0
    last_measure = time.time()
    mouse_pos = np.zeros(2)
    while running:
        frames += 1
        if time.time() - last_measure > 1:
            last_measure += 1
            print(frames)
            frames = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = np.array(event.pos)
        radius = time.time()*20 % 350

        #mouse_pos = np.array([256, 256])
        screen.fill((255, 255, 255))
        item_count = 0
        for item, point in quadtree.intersect(*(mouse_pos - radius), *(mouse_pos + radius)):
            item_count += 1
            pygame.draw.circle(screen, (255, 0, 0), point, 1)
            pass

        print(item_count)

        pygame.display.flip()


if __name__ == "__main__":
    main()
