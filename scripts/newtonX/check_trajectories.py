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
    # seek taken from 
    # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
        last_line = 'empty'

        if not os.path.isfile(traj_root + '/' + traj + '/md.out'):
            print(f'there is no md.out in {traj}')
            continue

        with open(traj_root + '/' + traj + '/md.out', 'rb') as f:
            try:  # catch OSError in case of a one line file 
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                print(f'error while reading {traj}')
                f.seek(0)
            last_line = f.readline().decode()

        # with open(traj_root + '/' + traj + '/md.out', 'r') as f:
        #     last_line = f.readlines()[-1]

        # read final message in md.out
        if 'Normal termination of Newton-X' in last_line:
            successfull.append(traj)
        else:
            # read time if there was a problem
            print('traj', traj, ' is a failed one')
            failed.append(traj)
    # print failed trajs with final time

if __name__ == '__main__':
    check_conclusion()
