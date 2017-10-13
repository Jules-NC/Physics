public class QT{
    private static final int MAX_PONTS = 1;
    private double[] p;  //Taille = 2
    private double[] b;  // Taille = 4
    private double[][] sB;
    private QT[] f;  // Taille: 4
    
    
    public QT(double[] _p, double[] _b, QT[] _f){
        this.p = _p;
        this.b = _b;
        this.sB = zones(this.b);
        this.f = _f;
    }
    
    public static boolean vide(QT q){
        return q == null;
    }
    
    public static boolean feuille(QT qt){
        return vide(qt.f[0]) && vide(qt.f[1]) && vide(qt.f[2]) && vide(qt.f[3]);
    }
    
    public static QT inserer(double[] point, double[] boundaries, QT quadTree){
        QT[] QTVide = {null, null, null, null} ;
        if(vide(quadTree)){
            return new QT(point, boundaries, QTVide);
        }
        int j = -1;  //Pour le débug
        for(int i=0; i<4; i++){
            if(pointInRect(point, quadTree.sB[i])){
                quadTree.f[i] = inserer(point, quadTree.sB[i], quadTree.f[i]);
            }
            if(quadTree.p != null){
                if(pointInRect(quadTree.p, quadTree.sB[i])){
                    quadTree.f[i] = inserer(quadTree.p, quadTree.sB[i], quadTree.f[i]);
                }
            }
        }
        quadTree.p = null;
        if(j==-1){
            System.out.print("CHEVAL:\n" + quadTree);
        }
        return quadTree;
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
        
        qt = inserer(p2, zone, qt);
        //qt.inserer(p3, zone, qt);
        System.out.println("1:\n" + qt.f[2].f[1]);
        //qt.inserer(p3, zone, qt);
        
    }
}
