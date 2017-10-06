from fps_master import regulate_fps
import math


class Modele:
    def __init__(self, *objets):
        self.objet_origine = Corps(masse=0)
        self.objets = objets
        self.routine()
        regulate_fps(self.routine, fps=1)

    def routine(self):
        for objet in self.objets:
            pass


class Vecteur:  # 2D
    def __init__(self, norme, angle):  # TRES TRES SALE
        self.norme = norme
        self.angle = angle

    def projection_cartesienne(self):
        x = math.cos(self.angle)*self.norme
        y = math.sin(self.angle)*self.norme
        return x, y

    def __add__(self, other):
        n_x = self.norme*math.cos(self.angle) + other.norme*math.cos(other.angle)
        n_y = self.norme*math.sin(self.angle) + other.norme*math.sin(other.angle)
        n_module = math.sqrt(n_x**2+n_y**2)
        n_angle = math.acos(n_x/n_module)
        return Vecteur(n_module, n_angle)

    def __mul__(self, other):
        x, y = self.norme*math.cos(self.angle), self.norme*math.sin(self.angle)
        x_p, y_p = other.norme*math.cos(other.angle), other.norme*math.sin(other.angle)
        return round(x*x_p+y*y_p, 10)  # For 0 with 2 normal vectors

    def __str__(self):
        return str((str(round(self.norme, 5)) + '.u', str(round(self.angle*180/math.pi, 5)) + '°'))


class Corps:
    def __init__(self, masse=1, diametre=0.1, x=0, y=0):
        self.masse = 1
        self.diametre = 1
        self.position = Vecteur(0, 0)
        self.vitesse = Vecteur(0, 0)
        self.acceleration = Vecteur(0, 0)

if __name__ == "__main__":
    a = Vecteur(math.sqrt(2), math.pi/4)
    b = Vecteur(1, 0)
    print('mult de:', a.projection_cartesienne(), '|', b.projection_cartesienne())
    print(a+b)
