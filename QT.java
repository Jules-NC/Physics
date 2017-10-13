public class QT{
    private double[] p;  // Coordonées représentatives du point (Taille = 1 point)
    private double[] b;  // Domaine de valeurs du noeud (Taille = 1 rectangle)
    private double[][] sB;  // Sous domaines de valeurs reliés aux fils (Taille: 4 rectangles)
    private QT[] f;  // fils du noeud actuel (Taille: 4 quadTrees)
    
    public double[] getP(){return this.p;}
    public void setP(double[] d){this.p = d;} 
    public double[] getSB(int i){return this.sB[i];}
    public QT getFi(int i){return this.f[i];}
    public void setFi(int i, QT q){this.f[i] = q;}
        
    public QT(double[] _p, double[] _b){
        QT[] QTVide = {null, null, null, null} ;
        this.p = _p;
        this.b = _b;
        this.sB = zones(this.b);
        this.f = QTVide;  // Arbre vide au départ
    }
    
    private static boolean vide(QT q){ return q == null; }
    
    public QT inserer(double[] point){
        for(int i=0; i<4; i++){
            if(vide(this.getFi(i)) && pointInRect(point, this.getSB(i)))
                this.setFi(i, new QT(point, this.getSB(i)));
            else if(pointInRect(point, this.getSB(i)))
                this.getFi(i).inserer(point);
            if(this.p != null){
                if(pointInRect(this.getP(), this.getSB(i))){
                    double[] pointTampon = this.getP();                
                    this.setP(null);  // Sinon boucle infinie car inserer verrait p!=null
                    this.inserer(pointTampon);
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
        double[] p1 = {1, 1};
        double[] p2 = {1.1, 1.1};
        double[] p3 = {1, 2};
        double[] zone = {0, 0, 5, 5};
        QT qt = new QT(p1, zone);
        
        qt.inserer(p2);
        qt.inserer(p3);
        
        System.out.println(qt);
    }
}
