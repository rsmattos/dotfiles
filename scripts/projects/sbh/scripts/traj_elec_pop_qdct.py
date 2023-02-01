#!/usr/bin/env python3

import sys
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def help_function(script_name):
    description = """
    ###################################################################################
    # script to create the electronic population from a single qdct trajectory        #
    # if the file name is not given, the script will attempt to read properties.hdf5  #
    # and if it fails, will try the analysis.hdf5                                     #
    #                                                                                 #
    # input:                                                                          #
    #   - analysis.hdf5 (qdct output) or                                              #
    #   - properties.hdf5 (reduced data with only the population)                     #
    #                                                                                 #
    # output: png plot with the electronic population                                 #
    #                                                                                 #
    # calling: {} [properties.hdf5|analysis.hdf5] 
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def dyn_analysis(file='analysis.hdf5'):
    S_tmp = pd.read_hdf(input, key='0001', mode='r')
    time = np.array(S_tmp.index) 
    elecs = np.array([x for x in S_tmp['elec_pop'].values])

    for i in list(h5py.File(input, 'r').keys())[1:]:
        S_tmp = pd.read_hdf(input, key=i, mode='r')
        time = np.append(time, np.array(S_tmp.index))
        elecs = np.append(elecs, np.array([x for x in S_tmp['elec_pop'].values]), axis=0)

    total = np.zeros(len(elecs))
    for i in range(elecs.shape[1]):
        total += elecs[:,i]
        plt.plot(time, elecs[:,i], label='S'+str(i))
    plt.plot(time, total, label='total')

    plt.title('qdct - elec_pop')
    plt.legend()
    plt.savefig('elec_pop.png')
    plt.close()

    return

def dyn_plot_elec_pop(file='properties.hdf5'):
    pop = pd.read_hdf(file, key='elec_pop', mode='r')
    pop.plot()
    plt.title('qdct - elec_pop')
    plt.legend()
    plt.savefig('elec_pop.png')
    plt.close()
    return

if __name__ == '__main__':

    if len(sys.argv) == 1:
        if os.path.exists('properties.hdf5'):
            dyn_plot_elec_pop()
        else:
            dyn_analysis()
    else:
        if str(sys.argv[1]) == '-h':
            help_function(sys.argv[0])

        file = str(sys.argv[1])
        if file == 'analysis.hdf5':
            dyn_analysis()
        elif file == 'properties.hdf5':
            dyn_plot_elec_pop()


