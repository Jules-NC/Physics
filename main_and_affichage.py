from pycallgraph.output import GraphvizOutput
from pycallgraph import PyCallGraph
from mecanique_classique import *
import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((950, 950))
pygame.display.set_caption('ORBITER 42: Space = See orbits | zqsd = moving | i,o = +,-')
DONE = False  # Boucle de simulation
DRAW = True  # Affichage des lignes
HOMOTETIE = 1
PAS = 1.5  # DE combien je me déplace
DEPLACEMENT = 1  # Sera scalé avec l'homotétie. Ne sert à rien je crois
MAX_I = 1000e10

modele = Modele()
REFERENT = modele.corps[0]
COLORS = [tuple(random.randint(40, 255) for _ in range(3)) for i in range(len(modele.corps))]
# COLORS = [(255, 255, 255), (0, 0, 0), (255, 0, 255)]
def main():
    global DONE
    global DRAW
    global HOMOTETIE
    global DEPLACEMENT
    i = 0
    points = []
    while not DONE and i < MAX_I:
        if DRAW:
            screen.fill((0, 0, 0))

    # ===========================================================================================
    # NE SERT PAS A LA SIMULATION: GESTION DES TOUCHES. ON REGARDE PAS
    # ===========================================================================================
        for event in pygame.event.get():  # On parcourt la liste de tous les évènements reçus
            if event.type == pygame.QUIT:  # Si un de ces évènements est de type QUIT
                DONE = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    DRAW = not DRAW
                    time.sleep(0.1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            modele.move(Vecteur(0, -DEPLACEMENT))
        if keys[pygame.K_s]:
            modele.move(Vecteur(0, DEPLACEMENT))
        if keys[pygame.K_q]:
            modele.move(Vecteur(-DEPLACEMENT, 0))
        if keys[pygame.K_d]:
            modele.move(Vecteur(DEPLACEMENT, 0))
        if keys[pygame.K_i]:
            HOMOTETIE /= 1.006
        if keys[pygame.K_o]:
            HOMOTETIE *= 1.006

        DEPLACEMENT = PAS * HOMOTETIE

    # ===========================================================================================
    # FIN GESTION DES TOUCHES. FIN TRUCS APS INTERESSANTS
    # ===========================================================================================

        i += 1
        if i%1 is 0:
            a = [[corp.position.x, corp.position.y] for corp in modele.corps]
            j = 0
            for c in a:
                c[0] = int(c[0]/abs(HOMOTETIE))
                c[1] = int(c[1]/abs(HOMOTETIE))
                pygame.draw.circle(screen, COLORS[j], c, 1, 1)
                j += 1
            #print(a)
            print('i: ', i)
            pygame.display.flip()
            time.sleep(0.0)
        c = modele.routine()

if __name__ == '__main__':
    #with PyCallGraph(output=GraphvizOutput()):
    main()
