import importlib
import adcpkrig
import numpy as np
import sklearn.gaussian_process
import pandas as pd
import pickle
import sys


largespace = sys.argv[1]
largeoverlap = sys.argv[2]
smallspace = sys.argv[3]
smalloverlap = sys.argv[4]

df = adcpkrig.createdf('vpts_sample.csv','bin_sample.csv')

np.random.seed(8)

rand = np.random.rand(len(df))
train = rand < 0.8 

traindf = df[train]

mygrid = adcpkrig.grid(traindf,5,5,0.5)
coords = adcpkrig.makechunks(mygrid,largespace,largeoverlap,smallspace,smalloverlap)

predicts = {}
tests = {}
coordsdict = {}

for i in range(len(coords)):
    
    testcoords = coords[i]

    xmin = testcoords[2]
    xmax = testcoords[3]
    ymin = testcoords[0]
    ymax = testcoords[1]
    zmin = 0
    zmax = mygrid.Z.shape[2]

    
    Xchunk,Ychunk,Zchunk = mygrid.chunk((xmin,xmax),(ymin,ymax),(zmin,zmax))
    predict,sigma,test = mygrid.interpchunk(Xchunk,Ychunk,Zchunk)
    predicts[i] = predict
    tests[i] = test
    coordsdict[i] = testcoords
    
    if np.isnan(predict[0]):
        print('{} blank'.format(i))
    else:
        print('{}/{}'.format(i,len(coords)))

with open('predicts.pickle', 'wb') as handle:
    pickle.dump(predicts, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('tests.pickle', 'wb') as handle:
    pickle.dump(tests, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('coordsdict.pickle', 'wb') as handle:
    pickle.dump(coordsdict, handle, protocol=pickle.HIGHEST_PROTOCOL)