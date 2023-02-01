#!/usr/bin/env python3

import pandas as pd
import h5py
import sys

def help_function(script_name):
    description = """
    ###################################################################################
    # script to extract the positions, velocities, nac, force and energies from a     #
    # given trajectory from the traj qdct output.                                     #
    #                                                                                 #
    # input:                                                                          #
    #      - trajs.hdf5 for a single trajectory                                       #
    #      - traj name ('00', '00b0')                                                 #
    #                                                                                 #
    # output:                                                                         #
    #       - positions.xyz in xyz format                                             #
    #       - velocities.xyz in xyz format                                            #
    #       - nac_10.xyz in xyz format                                                #
    #       - force_S1.xyz in xyz format                                              #
    #       - energies.dat
    #                                                                                 #
    # calling: {} [trajs.hdf5] [traj_name]                                            #
    #                                                                                 #
    # TODO: generalize the name of the force file to indicat the appropriate state    #
    #       generalize chice of nac vector                                            #
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def extract_trajs(in_file='trajs.hdf5', traj='00'):
    aum2elm = 1822.888515
    fs2au = 41.341374575751

    positions = []
    momenta = []
    nac_10 = []
    forces = []
    energies = []

    pos_string = 'positions_traj_'+traj
    mom_string = 'momenta_traj_'+traj
    nac_string = 'nac_10_traj_'+traj
    force_string = 'forces_i_traj_'+traj
    ene_string = 'energies_traj_'+traj

    for key in h5py.File(in_file, mode='r').keys():
        trajs = pd.read_hdf(in_file, mode='r', key=key)
        if pos_string in trajs.columns:
            positions.append(trajs[pos_string])
        if mom_string in trajs.columns:
            momenta.append(trajs[mom_string])
        if nac_string in trajs.columns:
            nac_10.append(trajs[nac_string])
        if force_string in trajs.columns:
            forces.append(trajs[force_string])
        if ene_string in trajs.columns:
            energies.append(trajs[ene_string])

    traj_00_positions = pd.concat(positions).drop_duplicates()
    traj_00_velocities = pd.concat(momenta).drop_duplicates()/aum2elm
    traj_00_nac_10 = pd.concat(nac_10).drop_duplicates()
    traj_00_forces = pd.concat(forces).drop_duplicates()
    traj_00_energies = pd.concat(energies).drop_duplicates()

    with open('traj_'+traj+'_positions.xyz', mode='w') as f:
        for time, row in traj_00_positions.iterrows():
            f.write('10 \n')
            f.write('time = {} fs \n'.format(time/fs2au))

            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                f.write('H \t {:>13.10f} \t {:12.7f} \t {:12.7f} \n'
                        .format(row['x_'+str(i)], row['y_'+str(i)], row['z_'+str(i)]))

    with open('traj_'+traj+'_velocities.xyz', mode='w') as f:
        for time, row in traj_00_velocities.iterrows():
            f.write('10 \n')
            f.write('time = {} fs \n'.format(time/fs2au))

            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                f.write('H \t {:>13.10f} \t {:12.7f} \t {:12.7f} \n'
                        .format(row['x_'+str(i)], row['y_'+str(i)], row['z_'+str(i)]))

    with open('traj_'+traj+'_nac_10.xyz', mode='w') as f:
        for time, row in traj_00_nac_10.iterrows():
            f.write('10 \n')
            f.write('time = {} fs \n'.format(time/fs2au))

            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                f.write('H \t {:>13.10f} \t {:12.7f} \t {:12.7f} \n'
                        .format(row['x_'+str(i)], row['y_'+str(i)], row['z_'+str(i)]))

    with open('traj_'+traj+'_forces_S1.xyz', mode='w') as f:
        for time, row in traj_00_forces.iterrows():
            f.write('10 \n')
            f.write('time = {} fs \n'.format(time/fs2au))

            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                f.write('H \t {:>13.10f} \t {:12.7f} \t {:12.7f} \n'
                        .format(row['x_'+str(i)], row['y_'+str(i)], row['z_'+str(i)]))

    with open('traj_'+traj+'_energies.dat', mode='w') as f:
        f.write('time \t S0 \t S1 \n')
        for time, row in traj_00_energies.iterrows():
            f.write('{:>8} \t {:>13.10f} \t {:>13.10f} \n'
                    .format(time/fs2au, row['0'], row['1']))

    return

if __name__ == '__main__':

    if len(sys.argv) == 1:
        extract_trajs()
    elif len(sys.argv) == 2:
        if str(sys.argv[1]) == '-h':
            help_function(sys.argv[0])

        in_file = str(sys.argv[1])
        extract_trajs(in_file)
    elif len(sys.argv) == 3:
        in_file = str(sys.argv[1])
        traj = str(sys.argv[2])
        extract_trajs(in_file, traj)


