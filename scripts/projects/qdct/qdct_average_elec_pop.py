#!/usr/bin/env python3

#########################################################################################
# script to read the population of each qdct trajectory 
# outputs the average on a csv file and plot them
#########################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def read_trajs(N):
    fs2au = 41.34137221718
    pops = {}
    for i in range(N):
        file = 'TRAJECTORIES/TRAJ'+str(i+1)+'/elec_pop.dat'
        if not os.path.isfile(file):
            continue
        
        pops[i] = pd.read_table(file, 
                                delimiter=r'\s+', 
                                skiprows=1, 
                                index_col=0,
                                names=['time (au)', 'norm', 'state 1', 'state 2'],
                                usecols=['time (au)', 'state 1', 'state 2']).dropna(axis=1)

    pop = pd.concat(pops, axis=1)

    average_pop1 = pop.xs('state 1', axis=1, level=1, drop_level=False).mean(axis=1)
    average_pop2 = pop.xs('state 2', axis=1, level=1, drop_level=False).mean(axis=1)
    
    avrg = pd.DataFrame()
    avrg['S0 population'] = average_pop1[average_pop1.index < 50*fs2au]
    avrg['S1 population'] = average_pop2[average_pop2.index < 50*fs2au]
    avrg['norm'] = avrg['S0 population'] + avrg['S1 population']

    avrg.to_csv('populations.csv')
    
    plt.plot(avrg.index.values/fs2au, avrg['S0 population'], label='S0')
    plt.plot(avrg.index.values/fs2au, avrg['S1 population'], label='S1')
    plt.plot(avrg.index.values/fs2au, avrg['norm'], label='norm')

    plt.xlabel('time (fs)')
        
    plt.title('average populations')
    plt.legend()
    plt.savefig('average_pop.png')
    plt.close()

    return


if __name__ == '__main__':

    N = int(sys.argv[1])

    print(N)

    read_trajs(N)
