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


class Vecteur:
    def __init__(self, angle=0, norme=1):
        self.angle = angle
        self.norme = norme

    def projection(self):
        x = math.cos(self.angle)*self.norme
        y = math.sin(self.angle)*self.norme
        return x, y

    def __add__(self, other):
        new_angle = (self.angle + other.angle)%360
        return Vecteur(angle=new_angle, norme=1)


class Corps:
    def __init__(self, masse=1, diametre=0.1, x=0, y=0):
        self.masse = 1
        self.diametre = 1
        self.position = Vecteur(0, 0)
        self.vitesse = Vecteur(0, 0)
        self.acceleration = Vecteur(0, 0)

a = Modele(Corps())