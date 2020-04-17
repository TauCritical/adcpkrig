import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import adcpkrig
import pickle
import pandas as pd
import math
from matplotlib import gridspec


def MAE(A, F):
    return (abs(A-F).sum()/len(A))


def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

class analysis():
    def __init__(self,traindf,comparedf,chunkdims):
        self.traindf = traindf
        self.comparedf = comparedf
        self.mygrid = adcpkrig.grid(traindf,5,5,0.5)
        self.coords = adcpkrig.makechunks(self.mygrid,chunkdims[0],chunkdims[1],chunkdims[2],chunkdims[3])

    def load_data(self,runnumber):
        with open('{}_predicts_v_mag.pickle'.format(runnumber), 'rb') as handle:
            self.predicts_mag = pickle.load(handle)

        with open('{}_predicts_v_x.pickle'.format(runnumber), 'rb') as handle:
            self.predicts_x = pickle.load(handle)

        with open('{}_predicts_v_y.pickle'.format(runnumber), 'rb') as handle:
            self.predicts_y = pickle.load(handle)

        with open('{}_predicts_v_z.pickle'.format(runnumber), 'rb') as handle:
            self.predicts_z = pickle.load(handle)
        
        self.maketests()
        #with open('{}_tests.pickle'.format(runnumber), 'rb') as handle:
        #    self.tests = pickle.load(handle)


    def maketests(self):

        tests = {}
        
        for i in range(len(self.coords)):

            testcoords = self.coords[i]
            xmin = testcoords[2]
            xmax = testcoords[3]
            ymin = testcoords[0]
            ymax = testcoords[1]
            zmin = 0
            zmax = self.mygrid.Z.shape[2]

            Xchunk,Ychunk,Zchunk = self.mygrid.chunk((xmin,xmax),(ymin,ymax),(zmin,zmax))
            
            Xmax = Xchunk[0][-1][0]
            Xmin = Xchunk[0][0][0]

            Ymax = Ychunk[-1][0][0]
            Ymin = Ychunk[0][0][0]

            Zmax = Zchunk[0][0][-1]
            Zmin = Zchunk[0][0][0]

            test = np.stack([np.ravel(Xchunk),np.ravel(Ychunk),np.ravel(Zchunk)],axis=1)

            tests[i] = test
        
        self.tests = tests
            
        pass


    def interponechunk(self,chunknumber,vdir,kernelparams=None):
        testcoords = self.coords[chunknumber]
        xmin = testcoords[2]
        xmax = testcoords[3]
        ymin = testcoords[0]
        ymax = testcoords[1]
        zmin = 0
        zmax = self.mygrid.Z.shape[2]
        Xchunk,Ychunk,Zchunk = self.mygrid.chunk((xmin,xmax),(ymin,ymax),(zmin,zmax))
        predict1,sigma,test = self.mygrid.interpchunk(Xchunk,Ychunk,Zchunk,vdir,kernelparams)
        return predict1,sigma,test

    def readrawonechunk(self,chunknumber,vdir):
        df = self.traindf
        
        testcoords = self.coords[chunknumber]
        xmin = testcoords[2]
        xmax = testcoords[3]
        ymin = testcoords[0]
        ymax = testcoords[1]
        zmin = 0
        zmax = self.mygrid.Z.shape[2]

        Xchunk,Ychunk,Zchunk = self.mygrid.chunk((xmin,xmax),(ymin,ymax),(zmin,zmax))
        Xmax = Xchunk[0][-1][0]
        Xmin = Xchunk[0][0][0]

        Ymax = Ychunk[-1][0][0]
        Ymin = Ychunk[0][0][0]

        Zmax = Zchunk[0][0][-1]
        Zmin = Zchunk[0][0][0]

        chunkmeas = df.loc[(df.X >= Xmin) & (df.X <= Xmax) & 
                            (df.Y >= Ymin) & (df.Y <= Ymax) & 
                            (df.Z >= Zmin) & (df.Z <= Zmax),:].copy()
                        
        return chunkmeas[vdir]

    def accuracycompareonechunk(self,chunknumber,predict,vdir):
        
        test = self.tests[chunknumber]
        
        iv = predict.T
        ix = test[:,0]
        iy = test[:,1]
        iz = test[:,2]
        
        
        df = pd.DataFrame(ix)
        df.columns = ['X']
        df['Y'] = iy
        df['Z'] = iz
        df['v'] = iv

        testcoords = self.coords[chunknumber]
        xmin = testcoords[2]
        xmax = testcoords[3]
        ymin = testcoords[0]
        ymax = testcoords[1]
        zmin = 0
        zmax = self.mygrid.Z.shape[2]

        Xchunk,Ychunk,Zchunk = self.mygrid.chunk((xmin,xmax),(ymin,ymax),(zmin,zmax))
        Xmax = Xchunk[0][-1][0]
        Xmin = Xchunk[0][0][0]

        Ymax = Ychunk[-1][0][0]
        Ymin = Ychunk[0][0][0]

        Zmax = Zchunk[0][0][-1]
        Zmin = Zchunk[0][0][0]

        chunkmeas = df.loc[(df.X >= Xmin) & (df.X <= Xmax) & 
                            (df.Y >= Ymin) & (df.Y <= Ymax) & 
                            (df.Z >= Zmin) & (df.Z <= Zmax),:].copy()

        cdf = self.comparedf
        cdf = cdf.loc[(cdf.X >= Xmin) & (cdf.X <= Xmax) & 
                            (cdf.Y >= Ymin) & (cdf.Y <= Ymax) & 
                            (cdf.Z >= Zmin) & (cdf.Z <= Zmax),:].copy()

        cdf['X_i'] = cdf.X.apply(lambda row: chunkmeas.X[find_nearest(chunkmeas.X,row)])
        cdf['Y_i'] = cdf.Y.apply(lambda row: chunkmeas.Y[find_nearest(chunkmeas.Y,row)])
        cdf['Z_i'] = cdf.Z.apply(lambda row: chunkmeas.Z[find_nearest(chunkmeas.Z,row)])

        mergedf = pd.merge(cdf,df,left_on=['X_i','Y_i','Z_i'],
                                right_on=['X','Y','Z'],suffixes=('_meas','_model'))

        return mergedf
        

    def mergepredicts(self):
        predicts_mag = self.predicts_mag
        predicts_x = self.predicts_x
        predicts_y = self.predicts_y
        predicts_z = self.predicts_z

        Xarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))
        Yarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))
        Zarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))
        V_magarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))
        V_xarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))
        V_yarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))
        V_zarr = np.zeros(len(predicts_mag[0])*len(predicts_mag.keys()))


        for i in range(len(predicts_mag.keys())):
            predict_mag = predicts_mag[i]
            predict_x = predicts_x[i]
            predict_y = predicts_y[i]
            predict_z = predicts_z[i]
            
            test = self.tests[i]
            
            ivmag = predict_mag.T
            ivx = predict_x.T
            ivy = predict_y.T
            ivz = predict_z.T
            ix = test[:,0]
            iy = test[:,1]
            iz = test[:,2]
            
            Xarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = ix
            Yarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = iy
            Zarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = iz
            V_magarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = ivmag
            V_xarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = ivx
            V_yarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = ivy
            V_zarr[i*len(predicts_mag[0]):(i+1)*len(predicts_mag[0])] = ivz

        alldf = pd.DataFrame(Xarr)
        alldf.columns = ['X']
        alldf['Y'] = Yarr
        alldf['Z'] = Zarr
        alldf['v_mag'] = V_magarr
        alldf['v_x'] = V_xarr
        alldf['v_y'] = V_yarr
        alldf['v_z'] = V_zarr

        self.alldf = alldf.groupby(['X','Y','Z']).mean().reset_index()

    def showmap(self,depth,vdir='v_mag',chunknum=None,chunknum2=None,chunknum3=None):


        X=np.array(self.alldf.loc[self.alldf.Z==depth,:].X)
        Y=np.array(self.alldf.loc[self.alldf.Z==depth,:].Y)
        v=np.array(self.alldf.loc[self.alldf.Z==depth,:][vdir])

        X = np.reshape(X,(self.alldf.X.unique().shape[0],-1))
        Y = np.reshape(Y,(self.alldf.X.unique().shape[0],-1))
        v = np.reshape(v,(self.alldf.X.unique().shape[0],-1))

        #levels = mpl.ticker.MaxNLocator(nbins=15).tick_values(v.min(), v.max())

        h,w = mpl.figure.figaspect(X)
        fig,ax=plt.subplots(1,1,figsize=(w,h))

        cs = ax.contourf(X,Y,v,levels=20,figure=fig)
        cbar = fig.colorbar(cs)


        if chunknum:
            xmin = self.tests[chunknum][0][0]
            xmax = self.tests[chunknum][-1][0]
            ymin = self.tests[chunknum][1][1]
            ymax = self.tests[chunknum][-1][1]
            rect = mpl.patches.Rectangle((xmin,ymin),(xmax-xmin),(ymax-ymin),fill=False,
                                        color='k')
            ax.add_patch(rect)

        if chunknum2:
            xmin = self.tests[chunknum2][0][0]
            xmax = self.tests[chunknum2][-1][0]
            ymin = self.tests[chunknum2][1][1]
            ymax = self.tests[chunknum2][-1][1]
            rect = mpl.patches.Rectangle((xmin,ymin),(xmax-xmin),(ymax-ymin),fill=False,
                                        color='r')
            ax.add_patch(rect)

        if chunknum3:
            xmin = self.tests[chunknum3][0][0]
            xmax = self.tests[chunknum3][-1][0]
            ymin = self.tests[chunknum3][1][1]
            ymax = self.tests[chunknum3][-1][1]
            rect = mpl.patches.Rectangle((xmin,ymin),(xmax-xmin),(ymax-ymin),fill=False,
                                        color='b')
            ax.add_patch(rect)

        fig.show()

    def showchunk(self,chunknum,predict,depth):
        test = self.tests[chunknum]
        results = pd.DataFrame(predict.T)
        results['X'] = test[:,0]
        results['Y'] = test[:,1]
        results['Z'] = test[:,2]
        X=np.array(results.loc[results.Z==depth,:].X)
        Y=np.array(results.loc[results.Z==depth,:].Y)
        Z=np.array(results.loc[results.Z==depth,:][0])

        X = np.reshape(X,(results.Y.unique().shape[0],-1))
        Y = np.reshape(Y,(results.Y.unique().shape[0],-1))
        Z = np.reshape(Z,(results.Y.unique().shape[0],-1))
        levels = mpl.ticker.MaxNLocator(nbins=15).tick_values(Z.min(), Z.max())

        w,h = mpl.figure.figaspect(X)
        fig,ax = plt.subplots(1,1,figsize=(w,h))
        cs = ax.contourf(X,Y,Z,levels=levels)
        cbar = fig.colorbar(cs)
        fig.show()

        return True


    def calcaccuracy(self):
        comparedf = self.comparedf
        
        comparedf['X_i'] = comparedf.X.apply(lambda row: self.alldf.X[find_nearest(self.alldf.X,row)])
        comparedf['Y_i'] = comparedf.Y.apply(lambda row: self.alldf.Y[find_nearest(self.alldf.Y,row)])
        comparedf['Z_i'] = comparedf.Z.apply(lambda row: self.alldf.Z[find_nearest(self.alldf.Z,row)])

        
        self.accdf = pd.merge(comparedf,self.alldf,left_on=['X_i','Y_i','Z_i'],
                                right_on=['X','Y','Z'],suffixes=('_meas','_model'))

    def plotscatter(self,analysisnumber):
        fig = plt.figure(figsize=(16,16))

        gs = gridspec.GridSpec(2,2)
        ax = [0,1,2,3]
        ax[0] = plt.subplot(gs[0])
        ax[1] = plt.subplot(gs[1])
        ax[2] = plt.subplot(gs[2])
        ax[3] = plt.subplot(gs[3])

        #fig,ax = plt.subplots(2,2,figsize=(20,20))

        universfile = 'C:\\Fonts\\Univers-Condensed.ttf'
        universboldfile = 'C:\\Fonts\\Univers-CondensedBold.ttf'
        ticks_font = mpl.font_manager.FontProperties(fname=universfile,style='normal',size=16, weight='normal', stretch='normal')
        label_font = mpl.font_manager.FontProperties(family='Arial',style='normal',size=20, weight='normal', stretch='normal')
        title_font = mpl.font_manager.FontProperties(fname=universboldfile,style='normal',size=28, weight='bold', stretch='normal')

        plotnames = ['Velocity Magnitude','East Magnitude','North Magnitude','Vertical Magnitude']
        colnames = ['v_mag','v_x','v_y','v_z']

        maes = []

        for i,col in enumerate(colnames):
                        
            pax = ax[i]
            pax.scatter(self.accdf[col + '_meas'],self.accdf[col + '_model'])
            xmin = pd.Series(self.accdf[col + '_meas']).dropna().min()
            xmax = pd.Series(self.accdf[col + '_meas']).dropna().max()
            ymin = pd.Series(self.accdf[col + '_model']).dropna().min()
            ymax = pd.Series(self.accdf[col + '_model']).dropna().max()
            pax.plot([-10,10],[-10,10],'k-')
            
            lims = [np.array([xmin,ymin]).min(),np.array([xmax,ymax]).max()]
            
            pax.set_xlim(lims)
            pax.set_ylim(lims)
            
            pax.yaxis.set_tick_params(direction='in')
            pax.xaxis.set_tick_params(direction='in')
            
            plt.setp(pax.get_xticklabels(),fontproperties=ticks_font)
            plt.setp(pax.get_yticklabels(),fontproperties=ticks_font)
            
            
            measured = self.accdf[col + '_meas'].dropna()
            modeled = self.accdf[col + '_model'].dropna()
            mae = MAE(measured,modeled)
            maes.append(mae)
            
            
            pax.text(0.2,0.9,'{}\nMAE: {:.3f} m/s'.format(plotnames[i],mae),transform=pax.transAxes,fontproperties=ticks_font)

        fig.text(0.5, 0.1, 'Measured velocity, in meters per second', ha='center', va='center',fontproperties=label_font)
        fig.text(0.1, 0.5, 'Interpolated velocity, in meters per second', ha='center', va='center', rotation='vertical',fontproperties=label_font)

        gs.update(hspace=0.07)
        gs.update(wspace=0.07)

        fig.suptitle('Analysis number {}'.format(analysisnumber),fontproperties=title_font)
        fig.savefig('scatter_{}'.format(analysisnumber))
        fig.show()
    
    def compare1(self,predict,sparse,title1='Interpolated Grid',title2='Sparse Measurements'):
        fig,axs = plt.subplots(1,2,figsize=(8,4))

        axs[0].hist(predict,bins=20)
        axs[0].set_xlabel('Velocity, in meters per second')
        axs[0].set_title(title1)

        axs[1].hist(sparse,bins=20)
        axs[1].set_xlabel('Velocity, in meters per second')
        axs[1].set_title(title2)


    def compare2(self,predict,predict1,sparse):
        fig,axs = plt.subplots(1,3,figsize=(8,4))

        axs[0].hist(predict,bins=20)
        axs[0].set_xlabel('Velocity, in meters per second')
        axs[0].set_title('Interpolated Grid')

        axs[1].hist(predict1,bins=20)
        axs[1].set_xlabel('Velocity, in meters per second')
        axs[1].set_title('Interpolated Grid (local)')

        axs[2].hist(sparse,bins=20)
        axs[2].set_xlabel('Velocity, in meters per second')
        axs[2].set_title('Sparse Measurements')

    def compareall(self):
        pass
