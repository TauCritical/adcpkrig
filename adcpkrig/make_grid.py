import numpy as np

def makegrid(df):

    x = np.array(df.X)
    y = np.array(df.Y)
    z = np.array(df.Z)

    xdivisions = int((x.max()-x.min())/xspacing)+1
    ydivisions = int((y.max()-y.min())/yspacing)+1
    zdivisions = int((z.max()-z.min())/zspacing)+1

    xi = np.linspace(x.min(),x.max(),xdivisions)
    yi = np.linspace(y.min(),y.max(),ydivisions)
    zi = np.linspace(z.min(),z.max(),zdivisions)

    X, Y, Z = np.meshgrid(xi, yi, zi)

    return (X,Y,Z)