from pycallgraph.output import GraphvizOutput
from pycallgraph import PyCallGraph
import concurrent.futures
import numpy as np
import random
import math

# CONSTANTES:
G = 6.674e-11  # Constante de gravitation de moi
M_SOLEIL = 1.989e30
M_TERRE = 5.972e24
M_LUNE = 7.342e22
D_TERLUNE = 384400e3  # metres
D_TERSOL = 149.6e9  # metres
V_TERSOL = 29.79e3  # m/s
H = 1.


class Modele:
    def __init__(self):
        self.corps = []
        soleil = Corps(x=300, y=300, masse=M_SOLEIL)
        soleil2 = Corps(x=-D_TERSOL*10, y=300, masse=M_SOLEIL, vitesse=np.array([0, V_TERSOL*0.13]))
        terre = Corps(x=D_TERSOL, y=300, masse=M_TERRE, vitesse=np.array([0, V_TERSOL]))
        lune = Corps(x=D_TERSOL+D_TERLUNE, y=300, masse=M_LUNE, vitesse=np.array([0, V_TERSOL + 1023]))

        self.corps.append(terre)
        self.corps.append(lune)
        self.corps.append(soleil)
        self.corps.append(soleil2)

        # self.corps = [Corps(x=random.randint(0, D_TERLUNE), y = random.randint(0, D_TERLUNE),
        #     masse=random.randint(M_LUNE, M_TERRE), vitesse=np.array([0., random.randint(-2000, 2000.)]))
        #               for _ in range(11)]
        self.liaisons()

    def liaisons(self):
        for corp in self.corps:
            corps_a_ajouter = [cp for cp in self.corps if cp is not corp]
            for cp in corps_a_ajouter:
                corp.influences.append(cp)

    def routine(self):
        # function = self.corps[0].update
        # corps = [corp for corp in self.corps]
        # with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        #     executor.map(function, corps)
        for corp in self.corps:
            corp.update()

    def move(self, direction):
        for corp in self.corps:
            np.add(corp.position, direction, out=corp.position, casting="unsafe")
            #corp.position += direction


class Corps:
    def __init__(self, masse=1, x=0, y=0, vitesse=np.array([0, 0])):
        self.influences = []
        self.masse = masse
        # Conds initiales
        self.vitesse = vitesse
        self.position = np.array([x, y])

    def acceleration(self):
        acceleration = np.array([0, 0])
        for influence in self.influences:
            distance = np.linalg.norm(np.subtract(self.position, influence.position))
            if distance < 2:  # Prévient le npqr
                return np.array([0., 0])
            f1 = G*influence.masse  # TODO: PENSER A LA MASSE DU CORP (Ici annulée) ds le cas d'autres forces.
            d3 = math.pow(distance, 3)
            np.add(acceleration, np.multiply(np.subtract(influence.position, self.position), f1*1/d3),
                   out=acceleration, casting="unsafe")
            print(acceleration)
        return acceleration

    def update(self):
        # VIRIMACHIN
        acceleration0 = self.acceleration()
        #self.position += self.vitesse*H + acceleration0*((H**2)/2)
        np.add(self.position, np.add(self.vitesse*H, acceleration0*((H**2)/2)), out=self.position, casting="unsafe")
        acceleration1 = self.acceleration()
        #self.vitesse += (acceleration0 + acceleration1)*(H/2)
        np.add(self.vitesse, np.add(acceleration0, acceleration1*(H/2)), out=self.vitesse, casting="unsafe")
        # print('   |Vitesse:', self.vitesse)
        # EULER
        # self.vitesse += self.acceleration()
        # self.position += self.vitesse


def mod_h(i):
    global H
    H = H*i
    H = abs(H)


def get_h():
    return H


if __name__ == "__main__":
    terre = Corps(x=-1, y=-1, masse=10e10)
    satellite = Corps(x=1, y=0, masse=1)
    satellite.influences.append(terre)
    terre.influences.append(satellite)
    print('Pos1:', satellite.position)
    print('Vit1:', satellite.vitesse)
    print("SATELLITE:")
    print(satellite.acceleration())
    print("TERRE:")
    # terre.acceleration()
