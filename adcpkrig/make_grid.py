def makegrid(df):

    x = np.array(TrimmedDF.POINT_X)
    y = np.array(TrimmedDF.POINT_Y)
    z = np.array(TrimmedDF.depth)


    v_mag = np.array(TrimmedDF.v_mag)
    v_emag = np.array(TrimmedDF.v_emag)
    v_nmag = np.array(TrimmedDF.v_nmag)
    v_hdir = np.array(TrimmedDF.v_hdir)


    xdivisions = int((x.max()-x.min())/xspacing)+1
    ydivisions = int((y.max()-y.min())/yspacing)+1
    zdivisions = int((z.max()-z.min())/zspacing)+1


    xi = np.linspace(x.min(),x.max(),xdivisions)
    yi = np.linspace(y.min(),y.max(),ydivisions)
    zi = np.linspace(z.min(),z.max(),zdivisions)

    X, Y, Z = np.meshgrid(xi, yi, zi)

    return (X,Y,Z)