import math


# CONSTANTES:
G = 6.674e-11  # Constante de gravitation universelle
M_SOLEIL = 1.989e30
M_TERRE = 5.972e24
M_LUNE = 7.342e22


class Modele:
    def __init__(self):
        self.fps = 30
        self.corps = []
        terre = Corps(x=384400e3, y=384400e3*2, masse=M_TERRE, vitesse=Vecteur(0, math.pi/2))
        lune = Corps(x=384400e3*1.5, y=384400e3*2, masse=M_LUNE, vitesse=Vecteur(980, math.pi/2))

        lune.influences.append(terre)
        terre.influences.append(lune)

        self.corps.append(lune)
        self.corps.append(terre)

    def routine(self, affichage=False):
        coords = []
        for corp in self.corps:
            corp.update()
            if affichage:
                coords.append([corp.position.x(), corp.position.y()])
                #print('Coords:', coords)
        return coords

    def afficher(self):
        pass


class Vecteur:  # 2D
    def __init__(self, norme, angle):  # TRES TRES SALE
        self.norme = norme
        self.angle = angle

    def x(self):
        return self.norme*math.cos(self.angle)

    def y(self):
        return self.norme*math.sin(self.angle)

    def projection_cartesienne(self):
        return self.x(), self.y()

    def angle_between(self, other):
        x = other.x() - self.x()
        y = other.y() - self.y()
        return cart_to_pol(x, y)  # Radians

    def distance(self, other):
        return cart_to_pol(other.x() - self.x(), other.y() - self.y()).norme

    def __add__(self, other):
        x = other.x() + self.x()
        y = other.y() + self.y()
        return cart_to_pol(x, y)

    def __mul__(self, other):
        x, y = self.norme*math.cos(self.angle), self.norme*math.sin(self.angle)
        x_p, y_p = other.norme*math.cos(other.angle), other.norme*math.sin(other.angle)
        return x*x_p+y*y_p, 10  # For 0 with 2 normal vectors

    def __str__(self):  # PRINT IN DEGREES
        return str((str(round(self.norme, 5)) + '.u', str(round(self.angle*180/math.pi, 5)) + '°'))


class Corps:
    def __init__(self, masse=1, x=0, y=0, vitesse=Vecteur(0, 0)):
        self.influences = []
        self.masse = masse
        # Conds initiales
        self.acceleration = Vecteur(0, 0)
        self.vitesse = vitesse
        self.position = cart_to_pol(x, y)

    def update(self):
        for influence in self.influences:
            f1 = G*influence.masse / ((self.position.distance(influence.position)) ** 2) * self.masse
            f1 /= self.masse
            direction = self.position.angle_between(influence.position)
            direction.norme = f1*1
            self.acceleration = direction
        self.vitesse += self.acceleration
        self.position += self.vitesse

    def self_to_other_vector(self, other):
        return self.position.angle_between(other.position)


def cart_to_pol(x, y):
    if is_close(x, 0) and is_close(y, 0):
        theta = 0   # C kom ca vect nul => 0° incl
    elif x > 0 and y >= 0:
        theta = math.atan(y / x)
    elif x > 0 and y < 0:
        theta = math.atan(y / x) + 2 * math.pi
    elif x < 0:
        theta = math.atan(y / x) + math.pi
    elif x == 0 and y > 0:
        theta = math.pi / 2
    elif x == 0 and y < 0:
        theta = 3 * math.pi / 2
    norme = math.sqrt(x**2+y**2)
    return Vecteur(norme, theta)


def is_close(a, b, rel_tol=1e-15):
    dist = abs(b-a)
    return dist < rel_tol

if __name__ == "__main__":
    terre = Corps(x=100, y=200, masse=M_TERRE)
    satellite = Corps(x=100, y=0, masse=1, corps=terre)
    print('Pos1:', satellite.position)
    print('Vit1', satellite.vitesse)
    print('Accel1', satellite.acceleration)
    for a in range(10):
        satellite.update()
    print('Pos2:', satellite.position.y())
    print('Vit2', satellite.vitesse)
    print('Accel2', satellite.acceleration)
