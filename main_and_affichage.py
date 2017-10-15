from pycallgraph.output import GraphvizOutput
from pycallgraph import PyCallGraph
from mecanique_classique import *
import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((950, 700))
pygame.display.set_caption('ORBITER 42: Space = See orbits | zqsd = moving | i,o = +,-')
DONE = False  # Boucle de simulation
DRAW = False  # Affichage des lignes
HOMOTETIE = 449.6e6
PAS = 0.5  # DE combien je me déplace
DEPLACEMENT = 1  # Sera scalé avec l'homotétie. Ne sert à rien je crois
MAX_I = 1000

modele = Modele()
COLORS = [tuple(random.randint(40, 255) for _ in range(3)) for i in range(len(modele.corps))]
# COLORS = [(255, 255, 255), (0, 0, 0), (255, 0, 255)]
COORDONEES = []
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
            modele.move(np.array([0, -DEPLACEMENT]))
        if keys[pygame.K_s]:
            modele.move(np.array([0, DEPLACEMENT]))
        if keys[pygame.K_q]:
            modele.move(np.array([-DEPLACEMENT, 0]))
        if keys[pygame.K_d]:
            modele.move(np.array([DEPLACEMENT, 0]))
        if keys[pygame.K_i]:
            HOMOTETIE /= 1.009
        if keys[pygame.K_o]:
            HOMOTETIE *= 1.009
        if keys[pygame.K_p]:
            mod_h(-H)
        if keys[pygame.K_m]:
            mod_h(1.003)
        if keys[pygame.K_l]:
            mod_h(1/1.003)

        DEPLACEMENT = PAS * HOMOTETIE

    # ===========================================================================================
    # FIN GESTION DES TOUCHES. FIN TRUCS APS INTERESSANTS
    # ===========================================================================================

        i += 1
        if i%50 is 0:
            p = [[corp.position[0], corp.position[1]] for corp in modele.corps]
            COORDONEES.append(p)
            j = 0
            for c in p:
                 cx = int(c[0]/abs(HOMOTETIE))
                 cy = int(c[1]/abs(HOMOTETIE))
                 pygame.draw.circle(screen, COLORS[j], (cx, cy), 1, 1)
                 j += 1
            print('i: ', i,'PAS:', get_h())
            pygame.display.flip()
            c = modele.routine()

def saveTimeFlow(really):
    if not really:
        print('TimeFlow NOT saved !')
        return
    with open('record3.csv', 'w') as f:
        nbr_planetes = len(COORDONEES[0])
        for i in range(nbr_planetes):
            f.write('x' + str(i) + ',y' + str(i) + ',')
        for coords_planetes in COORDONEES:
            for coords_planete in coords_planetes:
                f.write(str(coords_planete[0]) + ',' + str(coords_planete[1]) + ',')
            f.write('\n')
    print('TimeFlow saved !')


if __name__ == '__main__':
    start_time = time.time()
    with PyCallGraph(output=GraphvizOutput()):
        main()
    print("Temps d'éxécution: ", round(time.time() - start_time, 5) , "s")
    saveTimeFlow(False)


