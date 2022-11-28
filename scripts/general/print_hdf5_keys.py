#!/usr/bin/env python3

import sys
import os
import h5py

def help_function(script_name):
    description = """
    ###################################################################################
    # script to print the keys of a given hdf5 file                                   #
    #                                                                                 #
    # input: hdf5 file                                                                #
    #                                                                                 #
    # output: print to screen the keys form the hdf5 file                             #
    #                                                                                 #
    # calling: {} hdf5_file 
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def get_keys(file):
    if os.path.exists(file):
        h5_file = h5py.File(file, 'r')

        print(h5_file.keys())

        return 
    else:
        print("The file {} doesn't exist".format(file))

if __name__ == '__main__':
    if str(sys.argv[1]) == '-h':
        help_function(sys.argv[0])

    file = str(sys.argv[1])
    get_keys(file)


