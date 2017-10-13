public class QT{
    private double[] p;  // Coordonées représentatives du point (Taille = 1 point)
    private double[] b;  // Domaine de valeurs du noeud (Taille = 1 rectangle)
    private double[] centreMasse ; // Centre de masse du noeud (Point x, y)
    private double masse; // Masse totale
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
        this.b = _b;
        this.sB = zones(this.b);
        this.f = QTVide;  // Arbre vide au départ
        
        this.centreMasse = null;
        this.masse = _masse;
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
        for(int i=0; i<4; i++){
            if(vide(this.getFi(i)) && pointInRect(point, this.getSB(i)))
                this.setFi(i, new QT(point, this.getSB(i), masse));
            else if(pointInRect(point, this.getSB(i)))
                this.getFi(i).inserer(point, masse);
            if(this.p != null){
                if(pointInRect(this.getP(), this.getSB(i))){
                    double[] pointTampon = this.getP();                
                    this.setP(null);  // Sinon boucle infinie car inserer verrait p!=null
                    this.inserer(pointTampon, masse);
                }
            }
        }
        return this;
    }    

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
        // [x; x'[ et [y; y'[
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
        
        qt.inserer(p2, 10);
        qt.inserer(p3, 10);
        qt.updateCentreMasse();
        System.out.println(qt);
    }
}
