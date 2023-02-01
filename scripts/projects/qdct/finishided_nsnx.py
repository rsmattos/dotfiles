#!/usr/bin/env python3

####################################################################################################
# script to check which trajectories concluded successfully and which didn't, using new NX.
####################################################################################################

import os

def check_conclusion():
    traj_root = 'TRAJECTORIES'
    successfull = []
    failed = []

    # read folders in TRAJECTORIES dir
    trajs = os.listdir(traj_root)

    for traj in trajs:
        with open(traj_root + '/' + traj + '/md.out', 'r') as f:
            lines = f.readlines()

            # read final message in md.out
            if 'Normal termination of Newton-X' in lines[-2]:
                successfull.append(traj)
            else:
                # read time if there was a problem
                print('traj', traj, ' is a failed one')
                failed.append(traj)

    # print failed trajs with final time

if __name__ == '__main__':
    check_conclusion()