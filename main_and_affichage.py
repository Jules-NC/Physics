from truc import *
import pygame
import time

COLORS = [(0, 0, 255), (0, 255, 0), (255, 255, 255)]
pygame.init()
screen = pygame.display.set_mode((750, 2050))
done = False
draw = True

modele = Modele()
i = 0
points = []
while not done:
    if draw:
        screen.fill((0, 0, 0))

    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == pygame.QUIT:  # Si un de ces événements est de type QUIT
            done = True
        elif event.type == pygame.KEYDOWN:
            draw = not draw

    i += 1
    if i%10 is 0:
        a = modele.routine(True)
        j = 0
        for c in a:
            c[0] = int(c[0]/1)
            c[1] = int(c[1]/1)
            pygame.draw.circle(screen, COLORS[j], c, 1, 1)
            j += 1
        print(a)
        print('i: ', i)
        pygame.display.flip()
    c = modele.routine(False)

import numpy as np
print(points)
import matplotlib.pyplot as plt
plt.scatter(*zip(*points))
plt.show()
