#!/usr/bin/env python3

import pandas as pd
import h5py
import sys
import os

def help_function(script_name):
    description = """
    ###################################################################################
    # script to read the nuclear amplitudes from the qdct output and save to the      #
    # properties file                                                                 #
    #                                                                                 #
    # input: analysis.hdf5 for a single trajectory                                    #
    #                                                                                 #
    # output: properties.hdf5 with the nuclear amplitudes                             #
    #                                                                                 #
    # calling: {} [analysis.hdf5] [properties.hdf5]
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def extract_coefs(in_file='analysis.hdf5', out_file='properties.hdf5'):
    if os.path.exists(out_file):
        keys = list(h5py.File('properties.hdf5', 'r').keys())
        if 'coefs' in keys:
            print('coefficients already extracted.')
            return

    keys = list(h5py.File(in_file, 'r').keys())
    S_tmp = pd.read_hdf(in_file, key=keys[0], mode='r')
    coefs = pd.DataFrame(S_tmp['coefs'].tolist(), index = S_tmp.index)

    for k in keys[1:]:
        S_tmp = pd.read_hdf(in_file, key=k, mode='r')
        tmp = pd.DataFrame(S_tmp['coefs'].tolist(), index = S_tmp.index)
        coefs = pd.concat([coefs, tmp])

    coefs.to_hdf('properties.hdf5', key='coefs', mode='a', complevel=9, complib='blosc:lz4')

    return

if __name__ == '__main__':

    if len(sys.argv) == 1:
        extract_coefs()
        
    elif len(sys.argv) == 2:
        if str(sys.argv[1]) == '-h':
            help_function(sys.argv[0])

        in_file = str(sys.argv[1])
        extract_coefs(in_file)

    elif len(sys.argv) == 3:
        in_file = str(sys.argv[1])
        out_file = str(sys.argv[2])
        extract_coefs(in_file, out_file)


