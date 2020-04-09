'''
@author: Ed Bulliner
'''

import pandas as pd

def createdf(vpts,bins):

    inputdf = pd.read_csv(vpts)
    
    masterbindf = pd.read_csv(bins,index_col=None)

    masterbindf.columns = ['ens_ID','bin','depth','v_mag',
                            'v_emag','v_nmag','v_vcomp','v_hdir',
                            'v_error']

    moddf = masterbindf.copy()

    outputcols = ['POINT_X','POINT_Y','depth','v_mag',
                    'v_emag','v_nmag','v_hdir']
    outputdf = moddf.merge(inputdf, on='ens_ID').loc[:,outputcols]
    outputdf.columns=['X','Y','Z','v_mag','v_x','v_y','v_z']
    outputdf.Z = outputdf.Z * -1

    return outputdf

    