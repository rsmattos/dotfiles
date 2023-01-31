#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import random
import os
import sys

def read_trajs(subset):
    pops = {}
    for i in subset:
        print('reading file simulation_'+str(i)+'_elec_pop.dat')
        file = 'qdct_simulations/simulation_'+str(i)+'_elec_pop.dat'
        pops[i] = pd.read_table(file, delimiter=r'\s+', skiprows=1, index_col=0,
                                names=['time (au)', 'norm', 'state 1', 'state 2'],
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
    plt.savefig('average_pop.png')
    plt.close()

    return

def determine_subset(N, n):
    successful_trajs = []

    for i in range(1, N+1):
        file = 'qdct_simulations/simulation_'+str(i)+'_elec_pop.dat'
        if os.path.isfile(file):
            successful_trajs.append(i)

    print('list of successful trajectories')
    print(successful_trajs)
    if n == 0:
        return successful_trajs

    for i in range(100000):
        subset = []
    
        j = 0
        while j < n:
            new_num = random.randint(1, N)

            if not new_num in successful_trajs:
                break
            
            if not new_num in subset:
                subset.append(new_num)
                j += 1

#        print(subset)
        if len(subset) == n:
            break

    print('after ', i, 'iterations, the subset of trajectories chosen is ', subset)

    return subset

if __name__ == '__main__':

    N = int(sys.argv[1])
    n = int(sys.argv[2])

    subset = determine_subset(N, n)

    if n == 0:
        read_trajs(subset)
    elif len(subset) != n:
        print('not enough trajectories selected for the subset, try again')
    else:
        read_trajs(subset)
