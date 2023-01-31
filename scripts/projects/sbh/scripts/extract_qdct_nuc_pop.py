#!/usr/bin/env python3

import pandas as pd
import h5py
import sys
import os

def help_function(script_name):
    description = """
    ###################################################################################
    # script to read the nuclear population from the qdct output and save to the      #
    # properties file                                                                 #
    #                                                                                 #
    # input: analysis.hdf5 for a single trajectory                                    #
    #                                                                                 #
    # output: properties.hdf5 with the nuclear population                             #
    #                                                                                 #
    # calling: {} [analysis.hdf5] [properties.hdf5]
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def extract_nuc_pop(in_file='analysis.hdf5', out_file='properties.hdf5'):
    if os.path.exists(out_file):
        keys = list(h5py.File('properties.hdf5', 'r').keys())
        if 'nuc_pop' in keys:
            print('nuclear population already treated.')
            return

    keys = list(h5py.File(in_file, 'r').keys())
    S_tmp = pd.read_hdf(in_file, key=keys[0], mode='r')
    pop = pd.DataFrame(S_tmp['bf_pop'].tolist(), index = S_tmp.index)

    pop_transpher = pd.DataFrame(pop.sum(axis=1) - 1, columns=['norm_err'])
    pop = pop.diff(axis=0)
    pop_transpher['max'] = pop.max(axis=1)
    pop_transpher['min'] = pop.min(axis=1)
    pop_transpher['positive'] = pop.apply(lambda x : x[x > 0].sum(), axis=1)
    pop_transpher['negative'] = pop.apply(lambda x : x[x < 0].sum(), axis=1)
    pop_transpher['tot_transpher'] = pop_transpher[['positive', 'negative']].sum(axis=1)

    for k in keys[1:]:
        S_tmp = pd.read_hdf(in_file, key=k, mode='r')
        pop = pd.DataFrame(S_tmp['bf_pop'].tolist(), index = S_tmp.index)

        tmp = pd.DataFrame(pop.sum(axis=1) - 1, columns=['norm_err'])
        pop = pop.diff(axis=0)
        tmp['max'] = pop.max(axis=1)
        tmp['min'] = pop.min(axis=1)
        tmp['positive'] = pop.apply(lambda x : x[x > 0].sum(), axis=1)
        tmp['negative'] = pop.apply(lambda x : x[x < 0].sum(), axis=1)
        tmp['tot_transpher'] = tmp[['positive', 'negative']].sum(axis=1)
        
        pop_transpher = pd.concat([pop_transpher, tmp])

    pop_transpher.to_hdf('properties.hdf5', key='nuc_pop', mode='a', complevel=9, complib='blosc:lz4')

    return

if __name__ == '__main__':

    if len(sys.argv) == 1:
        extract_nuc_pop()
    elif len(sys.argv) == 2:
        if str(sys.argv[1]) == '-h':
            help_function(sys.argv[0])

        in_file = str(sys.argv[1])
        extract_nuc_pop(in_file)
    elif len(sys.argv) == 3:
        in_file = str(sys.argv[1])
        out_file = str(sys.argv[2])
        extract_nuc_pop(in_file, out_file)


