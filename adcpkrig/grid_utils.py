import numpy as np

class grid():
    def __init__(self,df,xspacing,yspacing,zspacing):

        x = np.array(df.X)
        y = np.array(df.Y)
        z = np.array(df.Z)

        #xspacing = 5
        #yspacing = 5
        #zspacing = 0.5

        xdivisions = int((x.max()-x.min())/xspacing)+1
        ydivisions = int((y.max()-y.min())/yspacing)+1
        zdivisions = int((z.max()-z.min())/zspacing)+1

        xi = np.linspace(x.min(),x.max(),xdivisions)
        yi = np.linspace(y.min(),y.max(),ydivisions)
        zi = np.linspace(z.min(),z.max(),zdivisions)

        self.X, self.Y, self.Z = np.meshgrid(xi, yi, zi)

    def chunk(self,xrange,yrange,zrange):

        xmin = xrange[0]
        xmax = xrange[1]
        ymin = yrange[0]
        ymax = yrange[1]
        zmin = zrange[0]
        zmax = zrange[1]

        Xchunk = self.X[ymin:ymax,xmin:xmax,zmin:zmax]
        Ychunk = self.Y[ymin:ymax,xmin:xmax,zmin:zmax]
        Zchunk = self.Z[ymin:ymax,xmin:xmax,zmin:zmax]

        Xmax = Xchunk[0][-1][0]
        Xmin = Xchunk[0][0][0]

        Ymax = Ychunk[-1][0][0]
        Ymin = Ychunk[0][0][0]

        Zmax = Zchunk[0][0][-1]
        Zmin = Zchunk[0][0][0]

        return (Xchunk,Ychunk,Zchunk)