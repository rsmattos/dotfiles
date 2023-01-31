#!/usr/bin/env python3

import sys
import h5py
import json

def help_function(script_name):
    description = """
    ###################################################################################
    # print the name of all trajectories spawned in the dynamic and the total number  #
    # of trajectories spawned                                                         #
    #                                                                                 #
    # input:                                                                          #
    #      - sim.hdf5                                                                 #
    #      - sim.json                                                                 #
    #                                                                                 #
    # output: print to screen the information                                         #
    #                                                                                 #
    # calling: {} [sim.hdf5|sim.json]
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def get_trajs_hdf5(file='sim.hdf5'):
    h5f = h5py.File(file, 'r')

    trajs = [x for x in h5f.keys() if 'traj_' in x]

    print(len(trajs))

    print(trajs)

    return

def get_trajs_json(file='sim.json'):
    with open(file, 'r') as f:
        data = json.load(f)

    print(len(data['traj_map']))

if __name__ == '__main__':

    if len(sys.argv) == 1:
        get_trajs_hdf5()
    else:
        if str(sys.argv[1]) == '-h':
            help_function(sys.argv[0])

        file = str(sys.argv[1])
        if file[-4:] == 'json':
            get_trajs_json(file)
        elif file[-4:] == 'hdf5':
            get_trajs_hdf5(file)


