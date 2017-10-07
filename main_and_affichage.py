from truc import *
import pygame
import time


#pygame.init()
#screen = pygame.display.set_mode((750, 450))
done = False

modele = Modele()
i = 0
points = []
with open('record', 'w') as f:
    while not done:
        if i%1000 is 0:
            points.append(modele.routine(i, affichage=True))
            print(str(points) + '\n')
            print(points[-1])
            print(i/1000000*100, '%')
        if i == 1000000:
            break
        modele.routine(False)
        i += 1

import numpy as np
print(points)
import matplotlib.pyplot as plt
plt.scatter(*zip(*points))
plt.show()
