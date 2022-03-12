import random
import time

import numpy as np
import pygame

RADIUS = 20


def main():
    items = []
    for i in range(20000):
        x = (random.random()) * 512
        y = (random.random()) * 512
        items.append((i, (x, y)))

    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    running = True
    frames = 0
    last_measure = time.time()
    mouse_pos = np.zeros(2)
    r_squared = RADIUS * RADIUS
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

        screen.fill((255, 255, 255))
        for item, point in items:
            if np.sum((mouse_pos - point) ** 2) < r_squared:
                pygame.draw.circle(screen, (255, 0, 0), point, 1)

        pygame.display.flip()


if __name__ == "__main__":
    main()
