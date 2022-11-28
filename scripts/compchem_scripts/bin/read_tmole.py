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
from geometric_param import *

def escf(args, paths):
    
    energy = defaultdict(dict)
    oscillator_str = defaultdict(dict)

    charge_transfer = pd.DataFrame()

    if args.theodore:
        tden_summ_header = pd.read_csv(paths[0][:-len(paths[0].split('/')[-1])]+'tden_summ.txt', sep='\s+', nrows=0).columns.tolist() 

    for i in range(len(paths)):
        p=[]

        file=open(paths[i],"r")
        lines=file.readlines()

        for line in range(len(lines)):
            # reads the parameter being evaluated
            if "| Atomic coordinate, charge and isotop information |" in lines[line]:
                if args.bond:
                    for atom in args.bond:
                        p.append(np.array([float(lines[line+3+atom].split()[0]),
                                           float(lines[line+3+atom].split()[1]),
                                           float(lines[line+3+atom].split()[2])]))
                    parameter=round(float(distance(p)))

                elif args.angle:
                    for atom in args.angle:
                        p.append(np.array([float(lines[line+3+atom].split()[0]),
                                           float(lines[line+3+atom].split()[1]),
                                           float(lines[line+3+atom].split()[2])]))
                    parameter=round(float(angle(p)))

                elif args.dihedral:
                    for atom in args.dihedral:
                        p.append(np.array([float(lines[line+3+atom].split()[0]),
                                           float(lines[line+3+atom].split()[1]),
                                           float(lines[line+3+atom].split()[2])]))
                    parameter=round(float(dihedral(p)))

                elif args.general:
                  	parameter=i+1

            # reads the ground state energy
            elif "              Ground state" in lines[line]:
                energy['GS'][parameter] = float(lines[line+3].split()[2])*27.2114

            elif "              I R R E P" in lines[line]:
                irrep = lines[line].split()[5]
                state = 1

            # reads the excited states energies
            elif ( "Excitation energy / eV:" ) in lines[line]:
                if lines[line-7].split()[1] == "singlet":
                    mult = "1"
                elif lines[line-7].split()[1] == "triplet":
                    mult = "3"

                if state > args.states:
                    continue
                energy[str(state)+'$^{'+mult+'}$'+irrep.upper()][parameter] = float(lines[line].split()[4])
                oscillator_str[str(state)+'$^{'+mult+'}$'+irrep.upper()][parameter] =  float(lines[line+9].split()[2])
                state += 1

        file.close()

        if args.theodore:
            tmp = pd.read_csv(paths[i][:-len(paths[i].split('/')[-1])]+'tden_summ.txt', sep='\s+', header=None, \
                              names=tden_summ_header, index_col='state', skiprows=2)
            charge_transfer[parameter] = tmp['CT']

    return pd.DataFrame(energy), pd.DataFrame(oscillator_str), charge_transfer.transpose()

def adc2(args, paths):
    
    energy = defaultdict(dict)
    dipole = defaultdict(dict)

    charge_transfer = pd.DataFrame()
    oscillator_str = pd.DataFrame()

    if args.theodore:
        tden_summ_header = pd.read_csv(paths[0][:-len(paths[0].split('/')[-1])]+'tden_summ.txt', sep='\s+', nrows=0).columns.tolist() 

    for i in range(len(paths)):
        p=[]
        project=[]

        file=open(paths[i],"r")
        lines=file.readlines()

        state = 0
        irrep = 'a'
        mult = '1'

        for line in range(len(lines)):

            # reads the parameter being evaluated
            if "| Atomic coordinate, charge and isotop information |" in lines[line]:
                if args.bond:
                    for atom in args.bond:
                        p.append(np.array([float(lines[line+3+atom].split()[0]),
                                           float(lines[line+3+atom].split()[1]),
                                           float(lines[line+3+atom].split()[2])]))
                    parameter=round(float(distance(p)))

                elif args.angle:
                    for atom in args.angle:
                        p.append(np.array([float(lines[line+3+atom].split()[0]),
                                           float(lines[line+3+atom].split()[1]),
                                           float(lines[line+3+atom].split()[2])]))
                    parameter=round(float(angle(p)))

                elif args.dihedral:
                    for atom in args.dihedral:
                        p.append(np.array([float(lines[line+3+atom].split()[0]),
                                           float(lines[line+3+atom].split()[1]),
                                           float(lines[line+3+atom].split()[2])]))
                    parameter=round(float(dihedral(p)))

                elif args.general:
                  	parameter=i+1
                    
                if args.project_dipole:
                    for atom in args.project_dipole:
                        project.append(np.array([float(lines[line+3+atom].split()[0]),
                                                 float(lines[line+3+atom].split()[1]),
                                                 float(lines[line+3+atom].split()[2])]))
                    
                    dipole['bond_x'][parameter],dipole['bond_y'][parameter],dipole['bond_z'][parameter] = project[1]-project[0]
                    
            # reads the ground state energy
            elif "            Total Energy    :" in lines[line]:
                energy['GS'][parameter] = float(lines[line].split()[3])*27.2114

            # reads the excited states energies
            elif ( "Excited state reached by transition:" ) in lines[line]:
                state = int(lines[line+1].split()[4])
                irrep = lines[line+1].split()[5]
                mult = lines[line+1].split()[6]
                if state > args.states:
                    continue
                energy[str(state)+'$^{'+mult+'}$'+irrep.upper()][parameter] = float(lines[line+2].split()[5])

            # reads dipole moment
            elif ("     Analysis of relaxed properties:") in lines[line]:
                if args.dipole:
                    dipole[str(state)+'$^{'+mult+'}$'+irrep.upper()+'_x'][parameter] = float(lines[line+7].split()[1]) / 0.393430307
                    dipole[str(state)+'$^{'+mult+'}$'+irrep.upper()+'_y'][parameter] = float(lines[line+8].split()[1]) / 0.393430307
                    dipole[str(state)+'$^{'+mult+'}$'+irrep.upper()+'_z'][parameter] = float(lines[line+9].split()[1]) / 0.393430307
                    
            # reads the corrected energies if there is solvent effect
            elif ( "COSMO-ADC(2) energy differences" ) in lines[line]:
                line += 4
                energy['GS'][parameter] = float(lines[line].split('|')[4])*27.2114
                line += 2

                while '----' in lines[line-1]:
                    state = int(lines[line].split('|')[3])
                    irrep = lines[line].split('|')[1].replace('*','').replace(' ','')
                    mult = lines[line].split('|')[2].replace(' ','')
                    if state > args.states:
                        break
                    energy[str(state)+'$^{'+mult+'}$'+irrep.upper()][parameter] = float(lines[line].split('|')[-2])
                    
                    line += 2

        file.close()

        if args.theodore:
            tmp = pd.read_csv(paths[i][:-len(paths[i].split('/')[-1])]+'tden_summ.txt', sep='\s+', header=None, \
                              names=tden_summ_header, index_col='state', skiprows=2)
            oscillator_str[parameter] = tmp['f']
            charge_transfer[parameter] = tmp['CT']

    return pd.DataFrame(energy), pd.DataFrame(dipole), oscillator_str.transpose(), charge_transfer.transpose()

def energy(args, paths):
    if not 'escf' in paths[0] and \
       not 'adc2' in paths[0] and \
       not 'ricc2' in paths[0]:
       print('Please specify the name of the file with the energies.')
       print('Acceptable files are escf.out, adc2.out or ricc2.out')
       exit()
    
    if 'escf' in paths[0]:
        return escf(args, paths)

    if 'adc2' in paths[0] or 'ricc2' in paths[0]:
        return adc2(args, paths)