from truc import *
import pygame
import time


pygame.init()
screen = pygame.display.set_mode((1300, 1200))
done = False

modele = Modele()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    modele.routine()
    #screen.fill((0, 0, 0))
    x_et_ys = []
    for corp in modele.corps:
        x = corp.position.x()
        y = corp.position.y()
        pygame.draw.circle(screen, (0, 128, 255), (int(x), int(y)), 1, 1)

    pygame.display.flip()