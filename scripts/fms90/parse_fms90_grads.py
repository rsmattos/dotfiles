#! /usr/bin/env python3

import pandas as pd
import numpy as np
import os

def read_fms90(input_file='Checkpoint.txt'):
    forces = []

    parse_force = False
    in_traj = False
    time  = 0
    force = 0
    traj  = 0

    with open(input_file, 'r') as f:
        file = f.readlines()

        for line in file:
            if parse_force:
                force = line.split()[0]
                forces[traj-1].append([time, force])
                parse_force = False

            if line[-13:] == 'Current time\n':
                time = line.split()[0]

            if line.split()[1:3] == ['Live', 'trajectory']:
                traj = int(line.split()[3])
                if traj > len(forces):
                    forces.append([])
                    print(f'appending trajectory {traj}')

                in_traj = True

            if line == ' # Force \n' and in_traj:
                parse_force = True
                in_traj = False

    return forces

def interpolate_forces(forces):
    for i in range(len(forces)):

        with open(f'PotEn.{i+1}', 'r') as f:
            lines = f.readlines()[1:]

            i_time = float(lines[0].split()[0])
            f_time = float(lines[-1].split()[0])
            time_step = float(lines[1].split()[0]) - float(lines[0].split()[0])

        time_df = pd.DataFrame(np.arange(i_time, f_time+time_step, time_step), columns=['time'])
        forces_df = pd.DataFrame(forces[i], columns=['time', 'force'], dtype=float)

        forces[i] = pd.merge(time_df, forces_df, how='outer', on='time') \
                            .interpolate(method='index', limit_direction='both')
    
    return forces

def save_forces(forces):
    for traj in range(len(forces)):
        with open(f'Force.{traj+1}', 'w') as f:
            f.write(f'# Time \t  gradx\n')

            f.write(forces[traj].to_csv(sep='\t', header=False, index=False))

    return

if __name__ == '__main__':
    forces = read_fms90()
    forces = interpolate_forces(forces)
    save_forces(forces)
