#!/usr/bin/env python3

#########################################################################################
# script to read the population of each FMS trajectory 
# outputs the average on a csv file and plot them
#########################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import sys

def read_trajs(N):
    fs2au = 41.34137221718
    pops = {}
    for i in range(N):
        pops[i] = pd.read_table('TRAJECTORIES/TRAJ'+str(i+1)+'/N.dat', 
                                delimiter=r'\s+', 
                                index_col=0, 
                                names=['time', 'state 1', 'state 2', 'norm'], 
                                skiprows=1).dropna(axis=1)

    pop = pd.concat(pops, axis=1)

    average_pop1 = pop.xs('state 1', axis=1, level=1, drop_level=False).mean(axis=1)
    average_pop2 = pop.xs('state 2', axis=1, level=1, drop_level=False).mean(axis=1)
    
    avrg = pd.DataFrame()
    avrg['S0 population'] = average_pop1
    avrg['S1 population'] = average_pop2
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

    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    else:
        N = int(input("Number of trajectories to consider: "))

    print(f'Averaging the occuparion of {N} trajectories available in TRAJECTORIES')

    read_trajs(N)
