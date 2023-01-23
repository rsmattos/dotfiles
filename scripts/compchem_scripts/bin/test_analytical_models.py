#! /usr/bin/env python3

# The script will calculate analytical models for a given point in space.
# Then it can comopare with values caluclated by an external MD software to check if the model implementation is correct.
# It should read the information generated by the external software in a text file and calculate the potential values for random positions present in the dataset.

import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import os
import sys

################### MODELS
def adiabat_general(H, dH):
    E = np.zeros(2)
    G = np.zeros(2)
    F12 = 0

    v11 = H[0,0]
    v22 = H[1,1]
    v12 = H[0,1]

    dv11 = dH[0,0]
    dv22 = dH[1,1]
    dv12 = dH[0,1]

    E[1] = np.sqrt(0.25*(v22*v22 - v11*v11)**2 + v12*v12)
    E[0] = -E[1]
    E += 0.5*(v11 + v22)

    G[1] = (0.25*(v22 - v11)*(dv22 - dv11) + v12*dv12)/   \
            np.sqrt(0.25*(v22 - v11)**2 + v12*v12)
    G[0] = -G[1]
    G += 0.5*(dv11 + dv22)

    F12 = ((v22 - v11)*(dv12) - v12*(dv22 - dv11))/      \
          ((v22 - v11)**2 + 4*v12*v12)

    return E, G, F12    

def calculate_values_at(x, model):
    if model == 'tully1':
        H, dH = diab_T1(x)
        E, G, F = adiabat_T1(H, dH)
    elif model == 'tully2':
        H, dH = diab_T2(x)
        E, G, F = adiabat_T2(H, dH)
    elif model == 'tully3':
        H, dH = diab_T3(x)
        E, G, F = adiabat_T3(H, dH)
    elif model == 'sbh':
        E, G, F = adiabat_short_sbh(x)
    else:
        print('please chose a supported model:')
        print('tully1')
        print('tully2')
        print('tully3')
        print('sbh')

        exit

    return E[0], E[1], G[0], G[1], F


#### Tully 1
def diab_T1(x):
    H = np.zeros([2,2])
    dH = np.zeros([2,2])

    A = 0.01
    B = 1.6
    C = 0.005
    D = 1.
    
    if x > 0:
        H[0,0] = A*(1 - np.exp(-B*x))
        dH[0,0] = A*B*np.exp(-B*x)
    else:
        H[0,0] = -A*(1 - np.exp(B*x))
        dH[0,0] = A*B*np.exp(B*x)

    H[1,1] = -H[0,0]
    dH[1,1] = dH[0,0]

    H[0,1] = C*np.exp(-D*x*x)
    dH[0,1] = -2*D*x*H[0,1]

    H[1,0] = H[0,1]
    dH[1,0] = dH[0,1]

    return H, dH

def adiabat_T1(H, dH):
    E = np.zeros(2)
    G = np.zeros(2)
    F12 = 0

    v11 = H[0,0]
    v12 = H[0,1]

    dv11 = dH[0,0]
    dv12 = dH[0,1]

    E[1] = np.sqrt(v11*v11 + v12*v12)
    E[0] = -E[1]

    G[1] = (v11*dv11 + v12*dv12)/np.sqrt(v11*v11 + v12*v12)
    G[0] = -G[1]

    F12 = 0.5*(v12*dv11 - v11*dv12)/(v11*v11 + v12*v12)

    return E, G, F12


#### Tully 2
def diab_T2(x):
    H = np.zeros([2,2])
    dH = np.zeros([2,2])

    A = 0.1
    B = 0.28
    C = 0.015
    D = 0.06
    E = 0.05

    # H[0,0] = 0
    # dH[0,0] = 0
    
    H[1,1] = -A*np.exp(-B*x*x) + E
    dH[1,1] = 2*A*B*x*np.exp(-B*x*x)

    H[0,1] = C*np.exp(-D*x*x)
    dH[0,1] = -2*D*x*H[0,1]

    H[1,0] = H[0,1]
    dH[1,0] = dH[0,1]

    return H, dH

def adiabat_T2(H, dH):
    E = np.zeros(2)
    G = np.zeros(2)
    F12 = 0

    v12 = H[0,1]
    v22 = H[1,1]

    dv12 = dH[0,1]
    dv22 = dH[1,1]

    E[1] = np.sqrt(0.25*v22*v22 + v12*v12)
    E[0] = -E[1]
    E += 0.5*v22

    G[1] = (0.25*v22*dv22 + v12*dv12)/   \
            np.sqrt(0.25*v22*v22 + v12*v12)
    G[0] = -G[1]
    G += 0.5*dv22

    F12 = (v22*dv12 - v12*dv22)/(v22*v22 + 4*v12*v12)

    return E, G, F12


#### Tully 3
def diab_T3(x):
    H = np.zeros([2,2])
    dH = np.zeros([2,2])

    A = 6E-4
    B = 0.1
    C = 0.9

    H[0,0] = A
    # dH[0,0] = 0

    H[1,1] = -A
    # dH[1,1] = 0

    if x < 0:
        H[0,1] = B*np.exp(C*x)
        dH[0,1] = C*H[0,1]
    else:
        H[0,1] = B*(2 - np.exp(-C*x))
        dH[0,1] = B*C*np.exp(-C*x) 
    
    H[1,0] = H[0,1]
    dH[1,0] = dH[0,1]
    
    return H, dH

def adiabat_T3(H, dH):
    E = np.zeros(2)
    G = np.zeros(2)
    F12 = 0

    v11 = H[0,0]
    v12 = H[0,1]

    dv12 = dH[0,1]

    E[1] = np.sqrt(v11*v11 + v12*v12)
    E[0] = -E[1]

    G[1] = v12*dv12/np.sqrt(v11*v11 + v12*v12)
    G[0] = -G[1]

    F12 = -0.5*v11*dv12/(v11*v11 + v12*v12)

    return E, G, F12


# Short 1D SBH
def adiabat_short_sbh(x):
    eps = 0.3
    nu0 = 0.05
    mass = 1

    freq = 4000/219474.63068
    coup = 0.7757824733

    E = np.zeros(2)
    G = np.zeros(2)
    F12 = 0

    eta = eps + coup*x
    e_diff = np.sqrt(eta*eta + nu0*nu0)
    f_diff = coup*eta/e_diff

    E += 0.5*mass*freq*freq*x*x
    E[0] -= e_diff
    E[1] += e_diff
    
    G += mass*freq*freq*x
    G[0] -= f_diff
    G[1] += f_diff

    F12 = -0.5*coup*nu0/(eta*eta + nu0*nu0)

    return E, G, F12


################### READING TEST DATA
#### Output from FMS90
def read_fms90(path_to_data = '.', traj='1'):
    A2bohr = 1.88973
    geometry_file = path_to_data+f'/positions.{traj}.xyz'
    energy_file = path_to_data+f'/PotEn.{traj}'
    coupling_file = path_to_data+f'/Coup.{traj}'

    os.system(f'echo "atom \t x \t y \t z" > tmp_geom')
    os.system(f'grep "H    " {geometry_file} >> tmp_geom')
    os.system(f'paste tmp_geom {energy_file} {coupling_file} > tmp')

    test_df = pd.read_csv('tmp', sep='\s+', 
                           usecols=[1, 4, 5, 6, 11, 12],
                           names=['pos', 'time', 'en_S0', 'en_S1', 'coup_21', 'coup_12'],
                           skiprows=1)

    os.system(f'rm tmp_geom tmp')

    # choose the non zero coupling to keep
    if np.max(np.abs(test_df['coup_12'])) > np.max(np.abs(test_df['coup_21'])):
        coup_idx = 'coup_12'
    else:
        coup_idx = 'coup_21'

    test_df['coup'] = test_df[coup_idx]
    test_df.drop(columns=['coup_12', 'coup_21'], inplace=True)

    # convert the positions to bohr
    test_df['pos'] = test_df['pos']*A2bohr

    return test_df

def read_mctdh(path_to_data = '.', pes_file = 'pes.dat'):
    pos = []
    en_s0 = []
    en_s1 = []

    with open(f'{path_to_data}/{pes_file}', 'r') as f:
        file = f.readlines()

        size = int(len(file)/2)

        for line in file[:size-1]:
            pos.append(line.split()[0])
            en_s0.append(line.split()[1])
        for line in file[size:-1]:
            en_s1.append(line.split()[1])

    return pd.DataFrame([pos, en_s0, en_s1], dtype=float).T. \
              rename(columns={0:'pos', 1:'en_S0', 2: 'en_S1'})

def read_test_data(params):
    if params.program == 'fms90':
        return read_fms90(params.inp_path, params.trajectory)
    elif params.program == 'mctdh':
        return read_mctdh(params.inp_path, params.pes_file)

    else:
        print(f'program not supported, please choose among:')
        print(f'none')
        print(f'fms90')
        print(f'mctdh')
        return

################### COMPARISON
def create_reference(x_min, x_max, model='tully1', step_size=0.1):
# creates a dataframe with the reference values in the range provided
# ideally the same range as the external values

    positions = np.arange(x_min, x_max, step_size)

    en_s0 = []
    en_s1 = []
    grad_s0 = []
    grad_s1 = []
    coup  = []

    for x in positions:
        en_s0_tmp, en_s1_tmp, grad_s0_tmp, grad_s1_tmp, coup_tmp = calculate_values_at(x, model)

        en_s0.append(en_s0_tmp)
        en_s1.append(en_s1_tmp)
        grad_s0.append(grad_s0_tmp)
        grad_s1.append(grad_s1_tmp)
        coup.append(coup_tmp)

    referende_df = pd.DataFrame()

    referende_df['pos'] = positions
    referende_df['en_S0'] = en_s0
    referende_df['en_S1'] = en_s1
    referende_df['grad_S0'] = grad_s0
    referende_df['grad_S1'] = grad_s1
    referende_df['coup'] = coup

    return referende_df

def test_values(out_path, test_df, amount=3, model='tully1', 
                sample_points=False, abs_coup=False):
# chooses random values from the external dataframe to compare with the refernece data
# one can give an amount to be randomly selected,
#    test-values(test_df, 10)
# or the sample_points list with the indices of the desired positions
#    test_values(test_df, sample_points=[1, 2, 3, 4])

    problem_points = []

    # choose whether to select random points for comparison or use the list given
    if not sample_points:
        sample_points = np.sort(random.sample(range(test_df.shape[0]), amount))

    # check if the test data has coupling vlaues
    if 'coup' in test_df.keys():
        use_coup = True
    else:
        use_coup = False

    with open(out_path+'/comparison.log', 'a') as f:
        f.write(f'points to be sampled: \n {sample_points} \n \n')

        for point in sample_points:
            values = test_df.iloc[point]
            pos_ex = values['pos']
            en_s0_ex = values['en_S0']
            en_s1_ex = values['en_S1']

            en_s0_ref, en_s1_ref, _, _, coup_ref = calculate_values_at(pos_ex, model)

            en_s0_diff = en_s0_ref - en_s0_ex
            en_s1_diff = en_s1_ref - en_s1_ex

            if abs(en_s0_diff) > 1e-6:
                problem_points.append(pos_ex)
            elif abs(en_s1_diff) > 1e-6:
                problem_points.append(pos_ex)

            f.write(f'\n for position {pos_ex} A, ')
            f.write(f'the values from the reference data and external data are: \n')
            f.write(f'en_S0(Eh): {en_s0_ref} \t {en_s0_ex}, ')
            f.write(f'with the difference: {en_s0_diff} \n')
            f.write(f'en_S1(Eh): {en_s1_ref} \t {en_s1_ex}, ')
            f.write(f'with the difference: {en_s1_diff} \n')

            if use_coup:
                coup_ex = values['coup']

                if abs_coup:
                    coup_diff = abs(coup_ref) - abs(coup_ex)
                else:
                    coup_diff = coup_ref - coup_ex

                if abs(coup_diff) > 1e-5:
                    problem_points.append(pos_ex)

                f.write(f'coup:      {coup_ref} \t {coup_ex}, with the difference: {coup_diff} \n')

        if len(problem_points) > 0:
            f.write('\n WARNING, significant differences between reference and test data. \n')
            f.write(f'The positions (Angs) that resulted in different values are \n')
            f.write(f'{problem_points} \n')
        else:
            f.write('\n SUCCESS, there is little or no difference between the reference and test data \n')

    return

def plot_comparison(reference_df, test_df, out_path, only_test=False, only_ref=False):
# make a plot of the energies in a file and coupling in another
# if the only_test option is true, will only plot the values of the test data
# if the only_ref option is true, will only plot the vlaues of the reference data
# if they are false, will plot the reference in the same image as test data
    if not only_ref:
        plt.plot(test_df['pos'], test_df['en_S0'], label='S0 test')
        plt.plot(test_df['pos'], test_df['en_S1'], label='S1 test')
    if not only_test:
        plt.plot(reference_df['pos'], reference_df['en_S0'], label='S0 ref')
        plt.plot(reference_df['pos'], reference_df['en_S1'], label='S1 ref')
    plt.ylabel('energy (Eh)')
    plt.xlabel('potision (bohr)')
    plt.legend()
    plt.savefig(f'{out_path}/potential_energy.png')

    # check if the test data has coupling vlaues
    if 'coup' in test_df.keys():
        plt.clf()
        if not only_ref:
            plt.plot(test_df['pos'], test_df['coup'], label='coupling fms90')
        if not only_test:
            plt.plot(reference_df['pos'], reference_df['coup'], label='coupling ref')
        plt.ylabel('coupling')
        plt.xlabel('potision (bohr)')
        plt.legend()
        plt.savefig(f'{out_path}/coupling.png')

class input_params:
    def __init__(self):
        self.program = 'none'
        self.inp_path = '.'
        self.out_path = '.'
        self.model = 'tully1'
        self.trajectory = '1'
        self.pes_file = 'pes.dat'
        self.test_amount = 100
        self.xmin = -10
        self.xmax = 10

def read_input(input_file = 'tests_models.inp'):
    p = input_params()

    if os.path.isfile(input_file):
        with open(input_file, 'r') as f:
            file = f.readlines()

            for line in file:
                if len(line.split()) == 0:
                    continue
                elif line.split()[0] == 'program':
                    p.program = line.split()[2]
                elif line.split()[0] == 'inp_path':
                    p.inp_path = line.split()[2]
                elif line.split()[0] == 'out_path':
                    p.out_path = line.split()[2]
                elif line.split()[0] == 'trajectory':
                    p.trajectory = line.split()[2]
                elif line.split()[0] == 'model':
                    p.model = line.split()[2]
                elif line.split()[0] == 'pes_file':
                    p.pes_file = line.split()[2]
                elif line.split()[0] == 'test_amount':
                    p.test_amount = int(line.split()[2])
                elif line.split()[0] == 'xmin':
                    p.xmin = int(line.split()[2])
                elif line.split()[0] == 'xmax':
                    p.xmax = int(line.split()[2])                

    else:
        with open(input_file, 'w') as f:
            f.write('######################################################################\n')
            f.write('# Input for the program to read the energies, gradient and coupling values\n')
            f.write('# calculated for analytical one dimensional problems with two states.\n')
            f.write('# the keyword and values should be separated by spaces and equal sign as\n')
            f.write('# as in template.\n')
            f.write('# The template has all possible options with their default values.\n')

            f.write('\n # General options, always used\n')
            f.write(f'program = {p.program}\n')
            f.write(f'inp_path = {p.inp_path}\n')
            f.write(f'out_path = {p.out_path}\n')
            f.write(f'# analytical model being teste, supported are:\n')
            f.write(f'# sbh, tully1, tully2, tully3\n')
            f.write(f'model = {p.model}\n')
            f.write(f'# number of points to randomly test \n')
            f.write(f'test_amount = {p.test_amount}\n')
            f.write(f'# range of x axis if no program is being read\n')
            f.write(f'xmin = {p.xmin}\n')
            f.write(f'xmax = {p.xmax}\n')

            f.write('\n # FMS90 specific options\n')
            f.write('# index of the trajectory to use, usually 1 because it has mor points.\n')
            f.write(f'trajectory = {p.trajectory}\n')

            f.write('\n # MTCDH specific options\n')
            f.write('# name of the file with the pes values.\n')
            f.write(f'pes_file = {p.pes_file}\n')

        exit()
    return p

if __name__ == '__main__':
    # input data that should be read from input file
    # inp_path = '/data/Rafael/test/mctdh/tully_3'
    # out_path = '/data/Rafael/test/mctdh/potential_validation/tully_3'
    # trajectory = '1'
    # model = 'tully3'
    # program = 'mctdh'

    if len(sys.argv) == 1:
        params = read_input()
    else:
        params = read_input(sys.argv[1])

    with open(params.out_path+'/comparison.log', 'w') as f:
        f.write('Analytical potential comparison for model:\n')
        f.write(f'{params.model}\n')
        f.write(f'from the program {params.program}\n')
        f.write(f'The input information are located in the folder:\n')
        f.write(f'{params.inp_path}\n')
        if params.program == 'fms90':
            f.write(f'The values taken are from trajectory: {params.trajectory}\n')
        f.write('\n')

    if params.program == 'none':
        xmin = params.xmin
        xmax = params.xmax
        only_ref = True
        test_df = {'coup': 0}
    
    else:
        only_ref = False
        # I want to read the external data from the given path
        test_df =  read_test_data(params)

        # print(test_df)
        # create the reference dataframe for comparison plots
        xmin = np.min(test_df['pos'])
        xmax = np.max(test_df['pos'])

    reference_df = create_reference(xmin, xmax, params.model)

    # chose random points to catch any error
    # can also be an equal distribution of points so we sweep the whole range
    # save the point comparison in a text file
    if not params.program == 'none':
        test_values(params.out_path, test_df, params.test_amount, params.model)

    # save the plots of energies and coupling on differenf files, with both methods
    plot_comparison(reference_df, test_df, params.out_path, only_ref=only_ref)


#TODO
# create template input file, to be filled to use
# read from input file
# read NX results