public class QT{
    private double[] p;  // Coordonées représentatives du point (Taille = 1 point)
    private double[] b;  // Domaine de valeurs du noeud (Taille = 1 rectangle)
    private double masse; // Masse totale du noeud
    private double[] centreMasse ; // Centre de masse du noeud (Point x, y)
    private double[][] sB;  // Sous domaines de valeurs reliés aux fils (Taille: 4 rectangles)
    private QT[] f;  // fils du noeud actuel (Taille: 4 quadTrees)
    
    public double[] getP(){return this.p;}
    public void setP(double[] d){this.p = d;} 
    public double[] getSB(int i){return this.sB[i];}
    public QT getFi(int i){return this.f[i];}
    public void setFi(int i, QT q){this.f[i] = q;}
    public double getMasse(){return this.masse;}
    public void addMasse(double d){this.masse += d;}
    public double[] getCentreMasse(){return this.centreMasse;}
   
    public QT(double[] _p, double[] _b, double _masse){
        QT[] QTVide = {null, null, null, null} ;
        this.p = _p;
        this.b = _b;  // Domaine du QuadTree.
        this.masse = _masse;
        this.centreMasse = null;  // ARBITRAIRE: Une feuile ne possède pas de "centre de masse".
        this.sB = zones(this.b);  // Création des sous-domaines de valeurs de la feuille.
        this.f = QTVide;  // Ce QT est une feuille.
    }
    
    private static boolean vide(QT q){ return q == null; }

    private static boolean feuille(QT q){ // Boucle for si besoin de généraliser à un n-tree
        return vide(q.getFi(0)) && vide(q.getFi(1)) && vide(q.getFi(2)) && vide(q.getFi(3));
    }
    
    private double[] updateCentreMasse(){
        double x = 0;
        double y = 0;
        double[] nul = {0, 0};
        double[] centreT = {-10000000000., -10000000000.}; // Pour débug
        this.masse = 0;  // Reset de la masse.
        for(int i=0; i<4; i++){
            if(vide(this.getFi(i)))
                continue;  // Un non objet n'a pas de masse. Passons le.
            if(feuille(this.getFi(i)))
                centreT = this.getFi(i).getP();
            else
                centreT = this.getFi(i).updateCentreMasse();
            double masseT = this.getFi(i).getMasse();
            x += centreT[0]*masseT;
            y += centreT[1]*masseT;
            this.addMasse(this.getFi(i).getMasse());
        }
        double[] res = {x /= this.getMasse(), y /= this.getMasse()};
        this.centreMasse = res;
        return res;
    }
    
    public QT inserer(double[] point, double masse){
        for(int i=0; i<4; i++){  // On itère sur les 4 sous emplacements.
            // Si le point a pour destination un sous-arbre vide, on crée cet arbre.
            if(vide(this.getFi(i)) && pointInRect(point, this.getSB(i))) 
                this.setFi(i, new QT(point, this.getSB(i), masse));
            // Si le point a pour destination un sous arbre non vide, on insère le point dans ce sous-arbre.
            else if(pointInRect(point, this.getSB(i)))
                this.getFi(i).inserer(point, masse);
            // Si cet arbre contient une valeur => ETAIT une feuille, on insère cette valeur dans le sous-arbre correspondant, 
            // puis on supprime cette valeur de l'arbre. Cet arbre devient ainsi un noeud.
            if(this.p != null){  // (INCERTAIN) Sert à éviter un nullPointerException dans pointInRect.
                if(pointInRect(this.getP(), this.getSB(i))){
                    double[] pointTampon = this.getP();                
                    this.setP(null);  // Sinon boucle infinie car inserer verrait p non null.
                    this.inserer(pointTampon, this.getMasse());
                }
            }
        }
        // La valeur de l'arbre n'est pas forcément située dans le même sous domaine que celui du point. On doit donc parcourir
        // les 4 sous-domaines, et donc retourner l'arbre ici.
        return this;
    } 

    // Renvoie les 4 sous rectangles d'un rectangle (Séparation au milieu).
    private static double[][] zones(double[] r){
        // Zones (Arbitraire):
        // |0, 1|
        // |2, 3|
        double dX = (r[0] + r[2])/2;
        double dY = (r[1] + r[3])/2;
        double[] z0 = {r[0], dY, dX, r[3]};
        double[] z1 = {dX, dY, r[2], r[3]};
        double[] z2 = {r[0], r[1], dX, dX};
        double[] z3 = {dX, r[1], r[3], dY};
        double[][] zones = {z0, z1, z2, z3};
        return zones;
    }
    
    private static boolean pointInRect(double[] p, double[] r){
        // Choix ARBITRAIRE d'inclusion/exclusion
        // [x; x'[ et [y; y'[ : sinon un point pourrait être présent dans plus d'un rectangle.
        return r[0]<=p[0] && p[0]<r[2] && r[1]<=p[1] && p[1]<r[3];
    }
   
    //+----------------------+
    //|INUTILE A PARTIR D'ICI|
    //+----------------------+
    public String toString(){
        String res = "|QuadTree:\n";
        if(this.p == null)  
            res += "   |null\n";
        else
            res += "   |Pt:   (" + this.p[0] + ", " + this.p[1] + ")\n";
        
        res += "   |Zone: (" + this.b[0] + ", " + this.b[1] + "; " +this.b[2] + ", "
            + this.b[3] + ")\n";
        
        res += "   |Fils: (" + !vide(this.f[0]) + ", " + !vide(this.f[1]) + ", " + !vide(this.f[2]) + ", "
            + !vide(this.f[3]) + ")";
        return res;
    }

    public static void main(){
        double[] p1 = {0, 0};
        double[] p2 = {0, 4};
        double[] p3 = {0, 8};
        double[] zone = {0, 0, 16, 16};
        QT qt = new QT(p1, zone, 10);
        
        qt.inserer(p2, 5);
        //qt.inserer(p3, 10);
        qt.updateCentreMasse();
        System.out.println(qt);
    }
}
