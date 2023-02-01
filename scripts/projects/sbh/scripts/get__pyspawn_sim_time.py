#!/usr/bin/env python3

import sys
import h5py

def help_function(script_name):
    description = """
    ###################################################################################
    # print to screen the final time of the simulation                                #
    #                                                                                 #
    # input: sim.hdf5                                                                 #
    #                                                                                 #
    # output: prints information to screen                                            #
    #                                                                                 #
    # calling: {} [sim.hdf5]
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def get_trajs(file='sim.hdf5'):
    h5f = h5py.File(file, 'r')

    last_time = h5f['traj_00']['time'][-1]

    print(last_time)

    return

if __name__ == '__main__':

    if len(sys.argv) == 1:
        get_trajs()
    else:
        if str(sys.argv[1]) == '-h':
            help_function(sys.argv[0])

        get_trajs(str(sys.argv[1]))


