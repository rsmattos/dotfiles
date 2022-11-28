#! /usr/bin/env python3

import pandas as pd
import numpy as np

###################      MANIPULATING DATA     ###################
# the excited states energies are in relation to the ground state in
# its own geometry, for the plot is necessary to find the lowest gound
# state energy, set it to zero and calculate all energies in relation
# to the lowest ground state

def energies(args, energy, oscillator_str):
    if args.program == 'orca':
        # sort excitation energies, since orca gives it mixed
        for i in energy.index:
            energy.loc[i, :] = energy.loc[i, :].sort_values().tolist()

    # sort energy values
    energy.sort_values(by = energy[energy.columns[0]].idxmin(), axis=1, inplace=True)

    # if oscillator has the same name for the headers, sort osc according to energy
    if not oscillator_str.empty:
        if sorted(list(energy.columns)) == sorted(list(oscillator_str.columns)):
            oscillator_str = oscillator_str.reindex(columns=energy.columns)

    # dislocates all ground states energies
    energy[energy.columns[0]] = energy[energy.columns[0]].subtract(energy[energy.columns[0]].min())

    # Add will sum the first column values to all columns, including the frist
    # the second line is to reset the first column to the non added original value
    tmp = energy.add(energy[energy.columns[0]], axis=0)
    tmp[energy.columns[0]] = energy[energy.columns[0]]

    return tmp.sort_index(), oscillator_str

def dipole(args, dipole):

    dipole.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in dipole.columns])

    states, pos = zip(*dipole.columns)
    states = list(dict.fromkeys(states))[1:]

    for state in states:
        dipole[state, 'abs']=np.sqrt( dipole[state, 'x']*dipole[state, 'x']+
                                      dipole[state, 'y']*dipole[state, 'y']+
                                      dipole[state, 'z']*dipole[state, 'z'] )

    if args.project_dipole:
        dipole['bond', 'abs']=np.sqrt( dipole['bond', 'x']*dipole['bond', 'x']+
                                       dipole['bond', 'y']*dipole['bond', 'y']+
                                       dipole['bond', 'z']*dipole['bond', 'z'] )

        for state in states:
            dipole[state, 'proj']=( dipole[state, 'x']*dipole['bond', 'x']+
                                    dipole[state, 'y']*dipole['bond', 'y']+
                                    dipole[state, 'z']*dipole['bond', 'z'] ) / dipole['bond', 'abs']

    return dipole.sort_index(axis=1)