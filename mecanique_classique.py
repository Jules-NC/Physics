import concurrent.futures
import random
import math

# CONSTANTES:
G = 3.674e-2  # Constante de gravitation de moi
M_SOLEIL = 1.989e30
M_TERRE = 5.972e24
M_LUNE = 7.342e22
H = 0.1


class Modele:
    def __init__(self):
        self.corps = [Corps(x=random.randint(0, 500), y=random.randint(0, 500), masse=random.randint(1000, 1000)) for a
            in range(50)]
        self.liaisons()

    def liaisons(self):
        for corp in self.corps:
            corps_a_ajouter = [cp for cp in self.corps if cp is not corp]
            for cp in corps_a_ajouter:
                corp.influences.append(cp)

    def routine(self):
        function = self.corps[0].update
        corps = [corp for corp in self.corps]
        with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
            executor.map(function, corps)

        for corp in self.corps:
            corp.update()

    def move(self, direction):
        for corp in self.corps:
            corp.position += direction


class Vecteur:  # 2D
    def __init__(self, x, y):  # TRES TRES SALE
        self.x = x
        self.y = y

    def angle_between(self, other):
        x = other.x - self.x
        y = other.y - self.y
        a = x*y
        b = math.sqrt(((other.x-self.x)**2)*((other.y-self.y)**2))
        if b == 0:
            b = 0.001
        return a/b

    def distance(self, other):
        return math.sqrt((other.x - self.x)**2+(other.y-self.y)**2)

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
        acceleration = Vecteur(0, 0)
        for influence in self.influences:
            if self.position.distance(influence.position) <= 0.001:  # OVERFLOW ACCELERATION
                return Vecteur(0, 0)
            f1 = G*influence.masse / ((self.position.distance(influence.position)) ** 2) * self.masse
            f1 /= self.masse
            angle = self.position.angle_between(influence.position)
            x = f1 * (influence.position.x - self.position.x)
            y = f1 * (influence.position.y - self.position.y)
            #print('Accel:', Vecteur(x, y))
            acceleration += Vecteur(x, y)
        return acceleration

    def update(self):
        acceleration0 = self.acceleration()
        self.position += self.vitesse*H + acceleration0*((H**2)/2)
        acceleration1 = self.acceleration()
        self.vitesse += (acceleration0 + acceleration1)*(H/2)

    def self_to_other_vector(self, other):
        return self.position.angle_between(other.position)

    def merge(self, other):
        self.masse += other.masse
        self.vitesse += other.vitesse
        other.position = Vecteur(10000, 0)


def is_close(a, b, rel_tol=1e-15):
    dist = abs(b-a)
    return dist < rel_tol

if __name__ == "__main__":
    terre = Corps(x=100, y=200, masse=1000)
    satellite = Corps(x=100, y=0, masse=1)
    satellite.influences.append(terre)
    print('Pos1:', satellite.position)
    print('Vit1', satellite.vitesse)
    for a in range(10):
        satellite.update()
    print('Pos2:', satellite.position.y)
    print('Vit2', satellite.vitesse)
    a  = Vecteur(0.01, 0.01)
    b = Vecteur(1, 1)
    print(a.angle_between(b)*180/math.pi)