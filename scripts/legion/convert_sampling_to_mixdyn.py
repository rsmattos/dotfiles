#!/usr/bin/env python3

import os

def read_uni_dim(file):

    pos = []
    mom = []

    with open(file) as f:
        for line in f.readlines()[1:]:
            pos.append([line.split()[0]])
            mom.append([line.split()[1]])

    return pos, mom


def read_multi_dim(file):
    with open(file) as f:
        lines = f.readlines()

    pos = []
    mom = []

    p = []
    m = []

    for line in lines:
        words = line.split()
        if '#' == words[0]:
            pos.append(p)
            mom.append(m)
            p = []
            m = []
            continue
        
        p.append(words[0])
        m.append(words[1])

    return pos, mom


def write_mixdyn(pos, mom):
    md_root = 'TRAJECTORIES_MIXDYN'
    os.makedirs(md_root, exist_ok=True)

    for i in range(len(pos)):
        os.makedirs(f'{md_root}/TRAJ{i+1}', exist_ok=True)

        with open(f'{md_root}/TRAJ{i+1}/geom.wxyz', mode='w') as f:
            f.write(f'{len(pos[i])}\n')
            f.write(f'UNITS=BOHR\n')
            for j in range(len(pos[i])):
                f.write(f'H  {pos[i][j]} \t 0.000000 \t 0.000000 \t 1.0000 \t 4.7\n')

        with open(f'{md_root}/TRAJ{i+1}/veloc.xyz', mode='w') as f:
            f.write(f'{len(mom[i])}\n')
            f.write(f'UNITS = bohr / au , momenta\n')
            for j in range(len(mom[i])):
                f.write(f'H  {mom[i][j]} \t 0.000000 \t 0.000000\n')

    return


###########################################################################################

if __name__ == '__main__':
    file = 'new_pos_mom_vel_mass'

    if os.path.exists('new_pos_mom_vel_mass'):
        file = 'new_pos_mom_vel_mass'
        pos, mom = read_uni_dim(file)
    elif os.path.exists('newcoord_mom_vel.txt'):
        file = 'newcoord_mom_vel.txt'
        pos, mom = read_multi_dim(file)

    write_mixdyn(pos, mom)
