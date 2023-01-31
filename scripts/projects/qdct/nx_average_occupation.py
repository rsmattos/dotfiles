#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def read_trajs(N=False, path='TRAJECTORIES'):
    occs = {}

    if N:
        for i in range(N):
            occs['Traj'+str(i+1)] = pd.read_table(path+'/TRAJ'+str(i+1)+'/RESULTS/energies.dat', delimiter=r'\s+', 
                                index_col=0, usecols=[0, 2], names=['time', 'state'], skiprows=2).dropna(axis=1)

    occ = pd.concat(occs, axis=1)

    average_occ1 = occ.isin([1]).sum(1)/occ.shape[1]
    average_occ2 = occ.isin([2]).sum(1)/occ.shape[1]

    occ['S0 occupation'] = average_occ1
    occ['S1 occupation'] = average_occ2
    occ['norm'] = average_occ1 + average_occ2
    occ[['S0 occupation', 'S1 occupation', 'norm']].to_csv('occupation.csv')

    plt.plot(average_occ1, label='S0')
    plt.plot(average_occ2, label='S1')
    plt.plot(occ['norm'], label='norm')

    plt.xlabel('time (fs)')
        
    plt.title('average occupation')
    plt.legend()
    plt.savefig('average_occupation.png')
    plt.close()

    return

if __name__ == '__main__':
    N = False
    path='TRAJECTORIES'

    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    elif len(sys.argv) == 3:
        N = int(sys.argv[1])
        path = str(sys.argv[2])

    print('Averaging the occuparion of {} trajectories available in {}'.format(N, path))
    read_trajs(N, path)
