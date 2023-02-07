#!/usr/bin/env python3

import os

def read_init_cond(file):

    pos = []
    mom = []

    with open(file) as f:
        for line in f.readlines()[1:]:
            pos.append(line.split()[0])
            mom.append(line.split()[1])

    return pos, mom


def write_fms_init_cond(pos, mom):
    fms_root = 'TRAJECTORIES_FMS'
    os.makedirs(fms_root)
    for i in range(len(pos)):
        os.makedirs(f'{fms_root}/TRAJ{i+1}', exist_ok=True)

        with open(f'{fms_root}/TRAJ{i+1}/Geometry.dat', mode='w') as f:
            f.write(f'   UNITS=BOHR\n')
            f.write(f'        1\n')
            f.write(f'H  {pos[i]} \t 0.000000 \t 0.00000 \n')
            f.write(f'#Momenta\n')
            f.write(f'   {mom[i]} \t 0.000000 \t 0.00000 \n')

    return

###########################################################################################

if __name__ == '__main__':
    file = 'new_pos_mom_vel_mass'

    if os.path.exists(file):
        pos, mom = read_init_cond(file)

    write_fms_init_cond(pos, mom)