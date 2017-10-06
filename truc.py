from fps_master import regulate_fps
import math


class Modele:
    def __init__(self, *objets):
        self.objet_origine = Corps(masse=0)
        self.objets = objets
        self.routine()
        self.fps = 30
        time_gap = 1/self.fps  # For simulation accuracy
        regulate_fps(self.routine, fps=self.fps)

    def routine(self):
        for objet in self.objets:
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

    def __add__(self, other):
        x = other.x() + self.x()
        y = other.y() + self.y()
        return cart_to_pol(x, y)

    def __mul__(self, other):
        x, y = self.norme*math.cos(self.angle), self.norme*math.sin(self.angle)
        x_p, y_p = other.norme*math.cos(other.angle), other.norme*math.sin(other.angle)
        return round(x*x_p+y*y_p, 10)  # For 0 with 2 normal vectors

    def __str__(self):  # PRINT IN DEGREES
        return str((str(round(self.norme, 5)) + '.u', str(round(self.angle*180/math.pi, 5)) + '°'))


class Corps:
    def __init__(self, masse=1, diametre=0.1, x=0, y=0):
        self.masse = masse
        self.diametre = diametre
        self.acceleration = Vecteur(0, 0)
        self.vitesse = Vecteur(0, 0)
        self.position = cart_to_pol(x, y)

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


def is_close(a, b, rel_tol=1e-11):
    dist = abs(b-a)
    return dist < rel_tol

if __name__ == "__main__":
    a = Vecteur(1, math.pi/2)
    b = Vecteur(math.sqrt(2), math.pi/4)
    print('ADDITION:', a, b, a+b)
    c1 = Corps(x=0, y=0)
    c2 = Corps(x=1, y=-1)
    print('POS1:', c1.position)
    print('POS2:', c2.position)
    #print(c1.self_to_other_vector(c2))
    #print(c2.self_to_other_vector(c1))
