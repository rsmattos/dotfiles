#!/usr/bin/env python3

#########################################################################################
# script to read the population of each NX trajectory 
# outputs the average on a csv file and plot them
#########################################################################################

import pandas as pd
import h5py
import matplotlib.pyplot as plt
import sys
import os

def read_trajs(N):
    pops = {}
    if os.path.isfile('TRAJECTORIES/TRAJ1/rho_1_2'):
        for i in range(N):
            pops[i] = pd.read_table('TRAJECTORIES/TRAJ'+str(i+1)+'/rho_1_2', 
                                    delimiter=r'\s+', 
                                    index_col=0, 
                                    names=['time', 'norm', 'real', 'imag'],
                                    skiprows=1).dropna(axis=1)
            
    pop = pd.concat(pops, axis=1)

    avrg = pd.DataFrame()
    avrg['Norm'] = pop.xs('norm', axis=1, level=1, drop_level=False).mean(axis=1)
#    avrg['S0_pop_std']    = pop.xs('state 1', axis=1, level=1, drop_level=False).std(axis=1)
#    avrg['S1_population'] = pop.xs('state 2', axis=1, level=1, drop_level=False).mean(axis=1)
#    avrg['S1_pop_std']    = pop.xs('state 2', axis=1, level=1, drop_level=False).std(axis=1)
#    avrg['Norm']          = avrg['S0_population'] + avrg['S1_population']

    avrg.to_csv('coherences.dat', sep='\t')
    
#    plt.plot(avrg['S0_population'], label='S0')
#    plt.plot(avrg['S1_population'], label='S1')
    plt.plot(avrg['Norm'], label='norm')

    plt.xlabel('time (fs)')
        
    plt.title('average populations')
    plt.legend()
    plt.savefig('average_coherence.png')
    plt.close()

    return

if __name__ == '__main__':

    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    else:
        N = int(input("Number of trajectories to consider: "))

    print(f'Averaging the population of {N} trajectories available in TRAJECTORIES')

    read_trajs(N)
