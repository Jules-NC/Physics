from truc import *
import pygame
import time


pygame.init()
screen = pygame.display.set_mode((750, 450))
done = False

modele = Modele()
i = 0
points = []
while not done:
    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == pygame.QUIT:  # Si un de ces événements est de type QUIT
            done = True
    i += 1
    if i%10000 is 0:
        c = modele.routine(True)
        c[0] = int(c[0]/3000000)
        c[1] = int(c[1]/3000000)
        print(c)
        pygame.draw.circle(screen, (0, 0, 255), c, 1, 1)
        pygame.display.flip()
    c = modele.routine(False)

import numpy as np
print(points)
import matplotlib.pyplot as plt
plt.scatter(*zip(*points))
plt.show()
