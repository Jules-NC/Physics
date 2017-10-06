import pygame
import truc


pygame.init()
screen = pygame.display.set_mode((1000, 700))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.draw.circle(screen, (0, 128, 255), (300, 30), 10, 3)

    pygame.display.flip()