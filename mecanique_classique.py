import concurrent.futures
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
        soleil2 = Corps(x=-D_TERSOL*10, y=300, masse=M_SOLEIL, vitesse=Vecteur(0, V_TERSOL*0.13))
        terre = Corps(x=D_TERSOL, y=300, masse=M_TERRE, vitesse=Vecteur(0, V_TERSOL))
        lune = Corps(x=D_TERSOL+D_TERLUNE, y=300, masse=M_LUNE, vitesse=Vecteur(0, V_TERSOL + 1023))

        self.corps.append(terre)
        self.corps.append(lune)
        self.corps.append(soleil)
        self.corps.append(soleil2)

        #self.corps = [Corps(x=random.randint(200, 700), y = random.randint(200, 500), masse=1000e9) for _ in range(3)]
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

        for corp in self.corps:
            corp.update()

    def move(self, direction):
        for corp in self.corps:
            corp.position += direction


class Vecteur:  # 2D
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def angle_between(self, other):
        return math.atan2(other.y, other.x) - math.atan2(self.y, self.x)

    def distance(self, other):
        distance = math.sqrt((other.x - self.x)**2+(other.y-self.y)**2)
        return distance

    def norme(self):
        return math.sqrt(self.x**2+self.y**2)

    def __add__(self, other):
        x = other.x + self.x
        y = other.y + self.y
        return Vecteur(x, y)

    def __mul__(self, other):
        if type(other) is float:  # Mult by a scalar
            return Vecteur(self.x*other, self.y*other)
        return self.x*other.x+self.y*other.y  # For 0 with 2 normal vectors

    def __str__(self):  # PRINT IN DEGREES
        return str((str(round(self.x, 5)) + '.x', str(round(self.y, 5)) + '.y'))


class Corps:
    def __init__(self, masse=1, x=0, y=0, vitesse=Vecteur(0, 0)):
        self.influences = []
        self.masse = masse
        # Conds initiales
        self.vitesse = vitesse
        self.position = Vecteur(x, y)

    def acceleration(self):
        acceleration = V_NUL
        for influence in self.influences:
            if self.position.distance(influence.position) < 2:  # OVERFLOW ACCELERATION
                return V_NUL
            f1 = G*influence.masse
            d3 = (influence.position.distance(self.position))**3
            x = f1*(influence.position.x - self.position.x)/d3
            y = f1 * (influence.position.y - self.position.y)/d3
            acceleration += Vecteur(x, y)
        return acceleration

    def update(self):
        # VIRIMACHIN
        acceleration0 = self.acceleration()
        self.position += self.vitesse*H + acceleration0*((H**2)/2)
        acceleration1 = self.acceleration()
        self.vitesse += (acceleration0 + acceleration1)*(H/2)
        # print('   |Vitesse:', self.vitesse)
        # EULER
        # self.vitesse += self.acceleration()
        # self.position += self.vitesse

    def merge(self, other):
        self.masse += other.masse
        self.vitesse += other.vitesse
        other.position = Vecteur(10000, 0)


def mod_h(i):
    global H
    H = H*i
    H = abs(H)

def get_h():
    return H

V_BASE = Vecteur(1, 0)
V_NUL = Vecteur(0, 0)
if __name__ == "__main__":
    terre = Corps(x=-1, y=-1, masse=10e10)
    satellite = Corps(x=1, y=0, masse=1)
    satellite.influences.append(terre)
    terre.influences.append(satellite)
    print('Pos1:', satellite.position)
    print('Vit1:', satellite.vitesse)
    print('Dist', satellite.position.distance(terre.position))
    print("SATELLITE:")
    print(satellite.acceleration())
    print("TERRE:")
    # terre.acceleration()
    a = Vecteur(300, 300)
    b = Vecteur(600, 300)
