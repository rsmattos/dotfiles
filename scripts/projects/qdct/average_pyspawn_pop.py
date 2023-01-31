#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def read_trajs(N):
    pops = {}
    for i in range(N):
        pops[i] = pd.read_table('TRAJECTORIES/TRAJ'+str(i+1)+'/N.dat', delimiter=r'\s+', 
                                index_col=0, names=['time (au)', 'state 1', 'state 2', 'norm'],
                                usecols=['time (au)', 'state 1', 'state 2']).dropna(axis=1)

    pop = pd.concat(pops, axis=1)

    average_pop1 = pop.xs('state 1', axis=1, level=1, drop_level=False).mean(axis=1)
    average_pop2 = pop.xs('state 2', axis=1, level=1, drop_level=False).mean(axis=1)
    
    avrg = pd.DataFrame()
    avrg['S0 population'] = average_pop1
    avrg['S1 population'] = average_pop2
    avrg['norm'] = avrg['S0 population'] + avrg['S1 population']

    avrg.to_csv('populations.csv')
    
    plt.plot(avrg.index.values/41.34137221718, avrg['S0 population'], label='S0')
    plt.plot(avrg.index.values/41.34137221718, avrg['S1 population'], label='S1')
    plt.plot(avrg.index.values/41.34137221718, avrg['norm'], label='norm')

    plt.xlabel('time (fs)')
        
    plt.title('average populations')
    plt.legend()
    plt.savefig('average_pop_'+str(N)+'.png')
    plt.close()

    return

if __name__ == '__main__':

    N = int(sys.argv[1])

    print(N)

    read_trajs(N)
