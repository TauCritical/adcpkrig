import numpy as np

def makechunks(grid,lsize,lmargin,smallsize,smallmargin):

    allshape = np.array(grid.X.shape)
    largestdim = allshape.argmax()
    secondlargestdim = allshape[-largestdim].argmax()

    largechunksize = lsize
    largechunkmargin = lmargin
    largechunkoverlap = largechunkmargin*2


    smallchunksize = smallsize
    smallchunkmargin = smallmargin
    smallchunkoverlap = smallchunkmargin*2

    zchunksize = None

    largechunks = int(allshape[largestdim]/(largechunksize-largechunkmargin))

    smallchunks = int(allshape[secondlargestdim]/(smallchunksize-smallchunkmargin))

    coords = []

    for i in range(largechunks):
        
        largestart = max([0,i*(largechunksize-largechunkmargin)])
        largeend = min([allshape[largestdim]-1,i*(largechunksize-largechunkmargin)+largechunksize])
        
        if largestart == 0:
            largeend = 0+largechunksize
        
        if largeend == allshape[largestdim]-1:
            largestart = allshape[largestdim]-1-largechunksize
        
        for j in range(smallchunks):
            smallstart = max([0,j*(smallchunksize-smallchunkmargin)])
            smallend = min([allshape[secondlargestdim]-1,j*(smallchunksize-smallchunkmargin)+smallchunksize])
            
            if smallstart == 0:
                smallend = 0 + smallchunksize
            
            if smallend == allshape[secondlargestdim]-1:
                smallstart = allshape[secondlargestdim]-1-smallchunksize
            
            if largestdim == 0:
                coords.append([largestart,largeend,smallstart,smallend])

            else:
                coords.append([smallstart,smallend,largestart,largeend])

    return coords