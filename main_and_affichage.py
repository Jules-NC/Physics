from truc import *
import pygame
import time

COLORS = [(0, 0, 255), (0, 255, 0), (255, 255, 255)]
pygame.init()
screen = pygame.display.set_mode((750, 2050))
pygame.display.set_caption('ORBITER 42: Space = See orbits | zqsd = moving | o,p = -,+')
done = False  # Boucle de simulation
draw = True  # Affichage des lignes
HOMOTETIE = 1

modele = Modele()
i = 0
points = []
while not done:
    if draw:
        screen.fill((0, 0, 0))

# ===========================================================================================
# NE SERT PAS A LA SIMULATION: GESTION DES TOUCHES. ON REGARDE PAS
# ===========================================================================================
    for event in pygame.event.get():  # On parcourt la liste de tous les évènements reçus
        if event.type == pygame.QUIT:  # Si un de ces évènements est de type QUIT
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw = not draw
                time.sleep(0.1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        modele.move(Vecteur(0.5, -math.pi/2))
    if keys[pygame.K_s]:
        modele.move(Vecteur(0.5, math.pi/2))
    if keys[pygame.K_q]:
        modele.move(Vecteur(0.5, math.pi))
    if keys[pygame.K_d]:
        modele.move(Vecteur(0.5, 0))
    if keys[pygame.K_o]:
        HOMOTETIE += 0.005
    if keys[pygame.K_p]:
        HOMOTETIE -= 0.005
# ===========================================================================================
# FIN GESTION DES TOUCHES. FIN TRUCS APS INTERESSANTS
# ===========================================================================================

    i += 1
    if i%1 is 0:
        a = modele.routine(True)
        j = 0
        for c in a:
            c[0] = int(c[0]/abs(HOMOTETIE))
            c[1] = int(c[1]/abs(HOMOTETIE))
            pygame.draw.circle(screen, COLORS[j], c, 1, 1)
            j += 1
        print(a)
        print('i: ', i)
        pygame.display.flip()
    c = modele.routine(False)
