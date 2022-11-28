#! /usr/bin/env python3

##############################################################################
#  Reads the geometry and energies from the utrbomole output, and outputs as a 
#  Dataframe
#  Input: enters the path and name of the files
#  Output: Dataframe with energies, column header has the states, vertical
#          index has the geometrica parameters
##############################################################################

import numpy as np
import pandas as pd
from collections import defaultdict

def energy(args, paths):
    
    energy = defaultdict(dict)
    oscillator_str = defaultdict(dict)

    charge_transfer = pd.DataFrame()

    if args.theodore:
        tden_summ_header = pd.read_csv(paths[0][:-len(paths[0].split('/')[-1])]+'tden_summ.txt', sep='\s+', nrows=0).columns.tolist() 

    for i in range(len(paths)):
        p=[]

        file=open(paths[i],"r")
        lines=file.readlines()

       	parameter=i+1

        for line in range(len(lines)):
            # reads the ground state energy
            if "# 1   1a                 DFTCI" in lines[line]:
                energy['GS'][parameter] = float(lines[line].split()[4])*27.2114
                continue

            elif ( "          DFTCI " ) in lines[line]:
                state = int(lines[line].split()[1])
                irrep = lines[line].split()[2]
                mult = str(1)
                if state > args.states:
                    continue
                energy[str(state)+'$^{'+mult+'}$'+irrep.upper()[-1]][parameter] = float(lines[line].split()[5])

        file.close()

        if args.theodore:
            tmp = pd.read_csv(paths[i][:-len(paths[i].split('/')[-1])]+'tden_summ.txt', sep='\s+', header=None, \
                              names=tden_summ_header, index_col='state', skiprows=2)
            charge_transfer[parameter] = tmp['CT']

    return pd.DataFrame(energy), pd.DataFrame(oscillator_str), charge_transfer.transpose()
