'''
The grid class contained in this file is the primary functionality for creating and interpolating grids
of acoustic Doppler current profiler sonar data with adcpkrig.

Upon initialization, we start with an input dataframe containing x, y, and z coordinates (generally assumed to be UTM),
along with v_mag (velocity magnitude) as well as individual x, y, and z velocity components at each measurement location.
Based on these measurements, a continuous regularly-spaced grid is created based on input specification of X, Y, and Z spacing
(assumed to be in the same units as coordinates, so meters for UTM)

The resulting object can then be used to create and interpolate chunks for arbitrary subsets of coordinates, allowing for
easy testing of multiple different sizes of interpolation chunks and varying overlap between chunks.

Author: Edward Bulliner
'''

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
        """Initializes a grid coordinate system in which measurements will be interpolated
        based on velocity values in v_mag (absolute magnitude) and v_x, v_y, and v_z vector components
        at measurement location. The created coordinate grids for interpolation are defined in extent to encompass all
        input measurements

        Args:
            df: a Pandas DataFrame containing x, y, and z coordinates of measurements and v_mag, v_x, v_y, and v_z
            xspacing: grid cell spacing in X direction, units matching coordinates in df (float)
            yspacing: grid cell spacing in Y direction, units matching coordinates in df (float)
            zspacing: grid cell spacing in Z direction, units matching coordinates in df (float)
        """

        self.df = df

        x = np.array(df.X)
        y = np.array(df.Y)
        z = np.array(df.Z)

        xdivisions = int((x.max()-x.min())/xspacing)+1
        ydivisions = int((y.max()-y.min())/yspacing)+1
        zdivisions = int((z.max()-z.min())/zspacing)+1

        xi = np.linspace(x.min(),x.max(),xdivisions)
        yi = np.linspace(y.min(),y.max(),ydivisions)
        zi = np.linspace(z.min(),z.max(),zdivisions)

        # Create coordinate grids using numpy's meshgrid function. This creates individual
        # 3d arrays in which the array values represent the dimension's value in that cell.
        # For example, the value at self.X[0][1][1] would be the minimum X coordinate in the dataset.
        # These arrays are used for the interpolation function in interpchunk
        self.X, self.Y, self.Z = np.meshgrid(xi, yi, zi)


    def chunk(self,xrange,yrange,zrange):
        """Creates chunked coordinate grids from the overall coordinate grid

        Args:
            xrange: tuple of numerical x indices (i.e. not UTM coordinates) that are range of chunk
            yrange: tuple of numerical y indices (i.e. not UTM coordinates) that are range of chunk
            zrange: tuple of numerical z indices (i.e. not UTM coordinates) that are range of chunk
        Returns:
            Tuple of length 3, where indexed values are:
            0 (Xchunk): a subset 3d array of X coordinates
            1 (Ychunk): a 1d array of standard deviation at predicted coordinates
            2 (Zchunk): a 1d array with entries of length 3 specifying X, Y, and Z coordinates
        """

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
        """Placeholder, not implemented. For differently specifying boundary chunks.
        Currently this is handled by code in make_chunks.py
        """
        pass

   
    def interpchunk(self,Xchunk,Ychunk,Zchunk,vdirection,kernelparams=None):
        """Interpolate one 'chunk' of ADCP data, with X, Y, and Z coordinate arrays
        that are a subset of the coordinate array created for the whole dataset
        using gaussian process regression

        Args:
            Xchunk: a subset 3d array of X coordinates at which to interpolate values for the chunk
            Ychunk: a subset 3d array of Y coordinates at which to interpolate values for the chunk
            Zchunk: a subset 3d array of Z coordinates at which to interpolate values for the chunk
            vdirection: a string specifying directionality of velocity data to interpolate {v_mag,v_x,v_y,v_z}
            kernelparams: (optional) a specification of the sklearn.gaussian_process.kernels method to use
        Returns:
            Tuple of length 3, where indexed values are:
            0 (predict): a 1d array of predicted values at coordinates specified by test
            1 (sigma): a 1d array of standard deviation at predicted coordinates
            2 (test): a 1d array with entries of length 3 specifying X, Y, and Z coordinates
        """

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
        
        # Note that as normalize_y=True, the large X/Y values in the coordinate arrays representing
        # UTM coordinates are normalized by removing mean and scaling to unit variance
        gp = sklearn.gaussian_process.GaussianProcessRegressor(kernel=kernel,normalize_y=True)
        
        try:
            gp.fit(np.array([x,y,z]).T,np.array(v))
            predict,sigma = gp.predict(test,return_std=True)

        # In case when interpolation fails due to no training data (i.e. outside measurement area
        # which does not cover whole grid), fill in NaN instead to allow masking
        except ValueError:
            predict = np.full(test.shape[0],np.nan)
            sigma = np.full(test.shape[0],np.nan)
            
        return (predict,sigma,test)

        