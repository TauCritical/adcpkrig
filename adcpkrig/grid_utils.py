import numpy as np
import sklearn.gaussian_process
from sklearn import preprocessing
import sys
import warnings
import os

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore" # Also affect subprocesses

class grid():
    def __init__(self,df,xspacing,yspacing,zspacing):

        self.df = df

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

    def boundchunk(self,Xchunk,Ychunk,Zchunk):
        pass
    
    def interpchunk(self,Xchunk,Ychunk,Zchunk,vdirection,kernelparams=None):

        Xmax = Xchunk[0][-1][0]
        Xmin = Xchunk[0][0][0]

        Ymax = Ychunk[-1][0][0]
        Ymin = Ychunk[0][0][0]

        Zmax = Zchunk[0][0][-1]
        Zmin = Zchunk[0][0][0]

        self.chunkmeas = self.df.loc[(self.df.X >= Xmin) & (self.df.X <= Xmax) & 
                            (self.df.Y >= Ymin) & (self.df.Y <= Ymax) & 
                            (self.df.Z >= Zmin) & (self.df.Z <= Zmax),:].copy()

        x = np.array(self.chunkmeas.X)
        y = np.array(self.chunkmeas.Y)
        z = np.array(self.chunkmeas.Z)
        v = np.array(self.chunkmeas[vdirection])

        test = np.stack([np.ravel(Xchunk),np.ravel(Ychunk),np.ravel(Zchunk)],axis=1)
        
        if not kernelparams:
            kernel=sklearn.gaussian_process.kernels.RationalQuadratic()
        else:
            kernel=kernelparams
        
        gp = sklearn.gaussian_process.GaussianProcessRegressor(kernel=kernel,normalize_y=True)
        
        try:
            gp.fit(np.array([x,y,z]).T,np.array(v))
            predict,sigma = gp.predict(test,return_std=True)
            
        except ValueError:
            predict = np.full(test.shape[0],np.nan)
            sigma = np.full(test.shape[0],np.nan)
            
        return (predict,sigma,test)

        