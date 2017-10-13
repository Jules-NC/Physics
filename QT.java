public class QT{
    private static final int MAX_PONTS = 1;
    private double[] p;  //Taille = 2
    private double[] b;  // Taille = 4
    private double[][] sB;
    private QT[] f;  // Taille: 4
    
    public double[] getP(){return this.p;}
    public void setP(double[] d){this.p = d;}
    
    public double[] getSB(int i){return this.sB[i];}
    
    public double[] getb(){return this.b;}
    public void setb(double[] d){this.b = d;}
    
    public QT[] getF(){return this.f;}
    public QT getFi(int i){return this.f[i];}
    public void setFi(int i, QT q){this.f[i] = q;}
    
    public QT(double[] _p, double[] _b, QT[] _f){
        this.p = _p;
        this.b = _b;
        this.sB = zones(this.b);
        this.f = _f;
    }
    
    private static boolean vide(QT q){
        return q == null;
    }
    
    private static boolean feuille(QT qt){
        return vide(qt.f[0]) && vide(qt.f[1]) && vide(qt.f[2]) && vide(qt.f[3]);
    }
    
    public QT inserer(double[] point, double[] boundaries){
        QT[] QTVide = {null, null, null, null} ;
        for(int i=0; i<4; i++){
            if(vide(this.f[i]) && pointInRect(point, this.sB[i])){
                this.f[i] = new QT(point, this.sB[i], QTVide);
            }
            else if(pointInRect(point, this.sB[i])){
                this.f[i].inserer(point, this.sB[i]);
            }
            if(this.p != null){
                if(pointInRect(this.p, this.sB[i])){
                    double[] point2 = this.p;                
                    this.p = null;  //Sinon boucle infinie car inserer verrait p!=null
                    this.inserer(point2, this.sB[i]);
                }
            }
        }
        return this;
    }    
    
    public static double[][] zones(double[] r){
        //p: x,y
        //r: x,y,x',y
        
        // Zones (Arbitraire):
        //|0, 1|
        //|2, 3|
        double dX = (r[0] + r[2])/2;
        double dY = (r[1] + r[3])/2;
        double[] z0 = {r[0], dY, dX, r[3]};
        double[] z1 = {dX, dY, r[2], r[3]};
        double[] z2 = {r[0], r[1], dX, dX};
        double[] z3 = {dX, r[1], r[3], dY};
        double[][] zones = {z0, z1, z2, z3};
        return zones;
    }
    
    public static boolean pointInRect(double[] p, double[] r){
        //[x; x'[ et [y; y'[
        return r[0]<=p[0] && p[0]<r[2] && r[1]<=p[1] && p[1]<r[3];
    }

    public String toString(){
        String res = "|QuadTree:\n";
        if(this.p == null)
            res += "   |null\n";
        else{
            res += "   |Pt:   (" + this.p[0] + ", " + this.p[1] + ")\n";
        }
        res += "   |Zone: (" + this.b[0] + ", " + this.b[1] + "; " +this.b[2] + ", "
            + this.b[3] + ")\n";
        
        res += "   |Fils: (" + !vide(this.f[0]) + ", " + !vide(this.f[1]) + ", " + !vide(this.f[2]) + ", "
            + !vide(this.f[3]) + ")";
        return res;
    }
    
    public static void main(){
        QT[] QTNull = {null, null, null, null};

        double[] p1 = {1, 1};
        double[] p2 = {2, 2};
        double[] p3 = {1, 2};
        double[] zone = {0, 0, 5, 5};
        QT qt = new QT(p1, zone, QTNull);
        
        qt.inserer(p2, zone);
        //qt.inserer(p3, zone, qt);
        System.out.println("1:\n" + qt.f[2].f[1]);
        //qt.inserer(p3, zone, qt);
        
    }
}
