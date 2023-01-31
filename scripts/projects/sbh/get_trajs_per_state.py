#!/usr/bin/env python3

import sys
import json

def get_traj_per_state(file='sim.json'):
    with open(file, 'r') as f:
        data = json.load(f)

    list_trajs = data['traj_map'].keys()

    s0 = 0
    s1 = 0
    total = len(list_trajs)

    for traj in list_trajs:
        if len(traj)%4 ==0:
            s0 += 1
        else:
            s1 += 1

    print('trajs in S0: {s0:5.2f}%, trajs in S1 {s1:5.2f}%'.format(s0 = 100*s0/total, s1 = 100*s1/total))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        get_traj_per_state()
    else:
        file = str(sys.argv[1])
        get_traj_per_state(file)
