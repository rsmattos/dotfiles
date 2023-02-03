#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [8, 6]
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.stats as st
import os
###

##############################################################################################
# Gaussian wavepacket
# Psi(x) = 1/(2*pi*del_x**2)**1/4 exp(-(x-x0)**2/(4*del_x**2)) exp(i*p0*x/hbar) 

# Wigner Function
# W(x,p) = 1/(pi*hbar) exp(-(x-x0)**2/(2*del_x**2)) exp(-(p-p0)**2/(2*del_p**2))
# del_p = hbar/(2*del_x)
##############################################################################################

# Universal Constants and Conversion 
hbar = 1.0
amu_to_au = 1822.8885150
cminv_to_au = 219474.63068
###

class parameters:
    def __init__(self):
        self.Ntrajs = 1
        self.x0 = 0
        self.p0 = 0
        self.del_x = 1
        self.del_p = 1
        self.nuclear_mass = 1
        self.random_seed = ''

def read_input():
    p = parameters()

    str1 = '*'
    print(str1*100)
    print('Please provide the following inputs to build the wavefunction')
    print(str1*100)

    # Number of trajectories to generate
    p.Ntrajs = int(input("Number of initial conditions to generate: "))

    # tries to read central position, momentum and mass from input in NX format
    if os.path.exists('geom.orig') and os.path.exists('veloc.orig'):
        with open('geom.orig', 'r') as f:
            line = f.readline()
            p.x0 = float(line.split()[2])
            p.nuclear_mass = float(line.split()[-1])

        with open('veloc.orig', 'r') as f:
            line = f.readline()
            p.p0 = float(line.split()[0])*p.nuclear_mass*amu_to_au
    else:
        p.x0 = float(input("Initial position (bohr): "))
        p.p0 = float(input("Initial momentum (a.u.): "))
        p.nuclear_mass = float(input("Nuclear mass to be used (electron mass unit): "))

    # del_x can be an input or default value
    p.del_x = input("Width of the Gaussian in position (default is 20/p): ")
    if p.del_x == '':
        p.del_x = 20/p.p0
    else:
        p.del_x = float(p.del_x)

    # Choice of random seed for reproducibility
    p.random_seed = input("Define integer to use as seed for random number generation: " )
    if p.random_seed == '':
        p.random_seed = np.random.randint(1000)
    else:
        p.random_seed = int(p.random_seed)

    np.random.seed(p.random_seed)

    p.del_p = hbar / (2.0 * p.del_x)

    print('')
    print('parameters provided:')
    print('x0      =', p.x0)
    print('p0      =', p.p0)
    print('mass    =', p.nuclear_mass*amu_to_au)
    print('del_x   =', p.del_x)
    print('del_p   =', p.del_p)
    print('npoints =', p.Ntrajs)
    print('iseed   =', p.random_seed)
    print('')

    return p
###############################################################################

# Wigner Distribution Function
def Wigner(x, p, x0, p0, del_x, del_p):
    W = 1.0/(np.pi*hbar) * np.exp(-(x-x0)**2 / (2.0*del_x**2)) * np.exp(-(p-p0)**2 / (2.0*del_p**2))
    return W
###

# Envelope function 
def envelope(var1, var2, x0,p0, del_x,del_p):
    loc_var1 = x0 - 4.0*del_x
    loc_var2 = p0 - 4.0*del_p
    scale_var1 = 8.0*del_x
    scale_var2 = 8.0*del_p
    # uniform distribution
    v1 = st.uniform.pdf(var1, loc=loc_var1, scale=scale_var1)
    v2 = st.uniform.pdf(var2, loc=loc_var2, scale=scale_var2)
    FXY = v1 * v2
    return FXY
###

## i changed the rejection sampling to have the option of choosing from the normal or uniform distribution 
## and also changed the loop so that I generate a predetermined number of initial conditions, instead of 
## making a predetermined number of attempts to sample
def rejection_sampling(Ntraj, x0,p0, del_x,del_p, scale):
    pos_accept = []
    mom_accept = []
    pos_reject = []
    mom_reject = []

    i = 0
    while i < Ntraj:
        r1 = np.random.uniform(x0 - 4.0*del_x, x0 + 4.0*del_x)
        r2 = np.random.uniform(p0 - 4.0*del_p, p0 + 4.0*del_p)

        u = np.random.uniform(0, scale*envelope(r1, r2, x0,p0, del_x,del_p))

        if u < Wigner(r1, r2, x0,p0,del_x,del_p):
            pos_accept.append(r1)
            mom_accept.append(r2)
            i += 1
        else:
            pos_reject.append(r1)
            mom_reject.append(r2)

    return np.array(pos_accept), np.array(mom_accept), np.array(pos_reject), np.array(mom_reject)

## function to write the initial conditions
def write_new_init_cond(pos_accepted, mom_accepted, mass):
    with open('new_pos_mom_vel_mass', mode='w') as f:
        f.write('#       pos \t            mom \t            vel \t             mass\n')
        for i in range(len(pos_accepted)):
            f.write(f'{pos_accepted[i]:>11.6f} \
\t {mom_accepted[i]:>14.11f} \
\t {mom_accepted[i]/(mass*amu_to_au):>14.11f} \
\t {mass:>14.11f}\n')

    return

## NX format
def write_nx_ns_init_cond(pos_accepted, mom_accepted, mass):
    os.makedirs('TRAJECTORIES_NX')
    for i in range(len(pos_accepted)):
        os.makedirs('TRAJECTORIES_NX/TRAJ'+str(i+1), exist_ok=True)

        with open('TRAJECTORIES_NX/TRAJ'+str(i+1)+'/geom.orig', mode='w') as f:
            f.write('H \t 1.0 \t {:>11.6f} \t 0.000000 \t 0.000000 \t {:>14.11f} \n'
                    .format(pos_accepted[i], mass))
        with open('TRAJECTORIES_NX/TRAJ'+str(i+1)+'/veloc.orig', mode='w') as f:
            f.write('\t {:>14.11f} \t 0.000000 \t 0.000000 \n'
                    .format(mom_accepted[i]/(mass*amu_to_au)))
    return

###############################################################################

if __name__ == '__main__':
    p = read_input()

    # Grid construction
    xgrid = np.arange(p.x0 - 10*p.del_x, p.x0 + 10*p.del_x, 0.1)
    pgrid = np.arange(p.p0 - 10*p.del_p, p.p0 + 10*p.del_p, 0.1)
    ###

    # Plotting the Wigner Function
    P, X = np.meshgrid(pgrid, xgrid)
    WDF = np.array(Wigner(X,P, p.x0, p.p0, p.del_x, p.del_p))

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf = ax.plot_surface(X, P, WDF, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0.1, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.view_init(30, 320)

    plt.title('WDF')
    plt.savefig('fig-wdf.png', dpi=300, bbox_inches='tight')
    ###

    # Plotting the Envelope function with WDF
    Envl = np.zeros((len(xgrid), len(pgrid)))

    for i in range(len(xgrid)): 
        for j in range(len(pgrid)): 
            var1 = xgrid[i]
            var2 = pgrid[j]
            Envl[i][j] = envelope(var1, var2, p.x0, p.p0, p.del_x, p.del_p) 
            
    scale = np.max(WDF) / np.max(Envl)
            
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf1 = ax.plot_surface(X, P, WDF, cmap='cool')
    surf2 = ax.plot_wireframe(X, P, scale*Envl, rstride=6, cstride=6)
    ax.view_init(30, -30)
    plt.savefig('fig-envelope_wdf.png', dpi=200, bbox_inches='tight')


    # Rejection Sampling 
    pos_accept, mom_accept, pos_reject, mom_reject = rejection_sampling(
            p.Ntrajs, p.x0, p.p0, p.del_x, p.del_p, scale)


    # outputting results
    write_new_init_cond(pos_accept, mom_accept, p.nuclear_mass)
    write_nx_ns_init_cond(pos_accept, mom_accept, p.nuclear_mass)


    # writting logs
    with open('init_cond.log', mode='w') as f:
        f.write('parameters provided:\n')
        f.write(f'x0      = {p.x0}\n')
        f.write(f'p0      = {p.p0}\n')
        f.write(f'mass    = {p.nuclear_mass*amu_to_au}\n')
        f.write(f'del_x   = {p.del_x}\n')
        f.write(f'del_p   = {p.del_p}\n')
        f.write(f'npoints = {p.Ntrajs}\n')
        f.write(f'iseed   = {p.random_seed}\n')

        f.write('\n\n')
        f.write('Amount of accepted trajectories:\n')
        f.write(f'positions: {len(pos_accept)} and momenta: {len(mom_accept)}\n')
        f.write('Amount of rejected trajectories:\n')
        f.write(f'positions: {len(pos_reject)} and momenta: {len(mom_reject)}\n')
        f.write('\n')
        f.write(f'Acceptance Score (%) = {len(pos_accept)/(len(pos_accept)+len(pos_reject))*100}')
        f.write('\n')


    # initial condition plot
    fig, ax = plt.subplots(figsize =(8, 6))
    plt.hist2d(pos_accept, mom_accept, bins =[25, 25], cmap = plt.cm.nipy_spectral)
    plt.colorbar()
    ax.set_xlabel('position') 
    ax.set_ylabel('momentum') 
    plt.savefig('fig-sampling.png', dpi=200, bbox_inches='tight')
