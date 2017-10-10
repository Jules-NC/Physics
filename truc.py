import math


# CONSTANTES:
G = 3.674e-2  # Constante de gravitation universelle
M_SOLEIL = 1.989e30
M_TERRE = 5.972e24
M_LUNE = 7.342e22
H = 6.0

class Modele:
    def __init__(self):
        self.fps = 30
        self.corps = []
        terre = Corps(x=300, y=400, masse=100000, vitesse=Vecteur(0.06, -math.pi/2))
        lune = Corps(x=400, y=400, masse=1000, vitesse=Vecteur(6.06, math.pi/2))
        new_horizon = Corps(x=350, y=486.6, masse=10, vitesse=Vecteur(6.06, 5*math.pi/6))
        #new_horizon = Corps(x=350, y=313.14, masse=10, vitesse=Vecteur(6.06, -5*math.pi/6))

        lune.influences.append(terre)
        lune.influences.append(new_horizon)

        terre.influences.append(lune)
        terre.influences.append(new_horizon)

        new_horizon.influences.append(terre)
        new_horizon.influences.append(lune)

        self.corps.append(new_horizon)
        self.corps.append(lune)
        self.corps.append(terre)

    def routine(self, affichage=False):
        coords = []
        for corp in self.corps:
            corp.update()
            #print(corp.position.y())
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
        if type(other) is float:
            return Vecteur(self.norme*other, self.angle)
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
        self.vitesse = vitesse
        self.position = cart_to_pol(x, y)

    def acceleration(self):
        acceleration = Vecteur(0, 0)
        for influence in self.influences:
            f1 = G*influence.masse / ((self.position.distance(influence.position)) ** 2) * self.masse
            f1 /= self.masse
            direction = self.position.angle_between(influence.position)
            direction.norme = f1
            acceleration += direction
        return acceleration

    def update(self):
        acceleration0 = self.acceleration()
        self.position += self.vitesse*H + acceleration0*((H**2)/2)
        acceleration1 = self.acceleration()
        self.vitesse += (acceleration0 + acceleration1)*(H/2)

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
