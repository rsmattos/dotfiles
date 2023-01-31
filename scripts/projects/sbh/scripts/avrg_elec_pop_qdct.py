#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import h5py
import sys

def help_function(script_name):
    description = """
    ###################################################################################
    # scipt to read and average the electronic population from different trajectories #
    # using qdct.                                                                     #
    #                                                                                 #
    # input: properties.hdf5 from each trajectory                                     #
    #                                                                                 #
    # output: png with the average elctronic population                               #
    #                                                                                 #
    # calling: {} TRAJ1/properties.hdf5 TRAJ2/properties.hdf5 ...
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def average_pop(file_paths, out_file='average_prop.hdf5'):
    trajs = []

    for traj in file_paths:
        trajs.append(pd.read_hdf(traj, mode='r', key='elec_pop'))

    average = sum(trajs)/len(trajs)

    average.to_hdf(out_file, key='elec_pop', mode='a', complevel=9, complib='blosc:lz4')
    
    time = average.index*2.418884254E-5

    plt.plot(time, average['S0'], label='S0')
    plt.plot(time, average['S1'], label='S1')
    plt.plot(time, average['norm'], label='norm')

    plt.xlabel('time (ps)')
        
    plt.title('average populations')
    plt.legend()
    plt.savefig('average_pop.png')
    plt.close()

    return

if __name__ == '__main__':
    if str(sys.argv[1]) == '-h':
        help_function(sys.argv[0])

    paths = sys.argv[1:len(sys.argv)]

    average_pop(paths)
