#!/usr/bin/env python3

import h5py
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def qdct_vs_pyspawn(pyspawn_file, qdct_file):
    pyspawn_pop = pd.read_csv(pyspawn_file, sep=' ', names=['S0', 'S1', 'norm', 'nan']).drop('nan', axis=1)
    
    max_time = pyspawn_pop.index[-1]

    qdct_pop = pd.read_hdf(qdct_file, key='elec_pop', mode='r')
    qdct_pop = qdct_pop.loc[qdct_pop.index < max_time+1E-3]

    plt.plot(qdct_pop['S0'], 'b-', label='qdct_S0')
    plt.plot(qdct_pop['S1'], 'b--', label='qdct_S1')
    plt.plot(qdct_pop['norm'], 'b-.', label='qdct_norm')

    plt.plot(pyspawn_pop['S0'], 'g-', label='pyspawn_S0')
    plt.plot(pyspawn_pop['S1'], 'g--', label='pyspawn_S1')
    plt.plot(pyspawn_pop['norm'], 'g-.', label='pyspawn_norm')

    plt.title('pyspawn vs qdct')
    plt.legend()
    plt.savefig('pyspawn_vs_qdct.png')
    plt.close()
    return

if __name__ == '__main__':

    if len(sys.argv) == 3:
        qdct_vs_pyspawn(sys.argv[1], sys.argv[2])

    else:
        raise Exception('Expected tha name of the pyspawn_file and qdct_file in this order')
