#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [8, 6]
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.stats as st
from scipy.interpolate import griddata
from scipy.stats import multivariate_normal
import os
###

# Universal Constants and Conversion 
hbar = 1.0
amu_to_au = 1822.8885150
cminv_to_au = 219474.63068
###

# Gaussian wavepacket
# Psi(x) = 1/(2*pi*del_x**2)**1/4 exp(-(x-x0)**2/(4*del_x**2)) exp(i*p0*x/hbar) 

# Wigner Function
# W(x,p) = 1/(pi*hbar) exp(-(x-x0)**2/(2*del_x**2)) exp(-(p-p0)**2/(2*del_p**2))
# del_p = hbar/(2*del_x)
###

str1 = '*'
print(str1*100)
print('Please provide the following inputs to build the wavefunction')
print(str1*100)

# tries to read central position, momentum and mass from input in NX format
if os.path.exists('geom.orig') and os.path.exists('veloc.orig'):
    with open('geom.orig', 'r') as f:
        line = f.readline()
        x0 = float(line.split()[2])
        nuclear_mass = float(line.split()[-1])

    with open('veloc.orig', 'r') as f:
        line = f.readline()
        p0 = float(line.split()[0])*nuclear_mass*amu_to_au
else:
    x0 = float(input("Initial position: "))
    p0 = float(input("Initial momentum: "))
    nuclear_mass = float(input("Nuclear mass to be used: "))

# del_x can be an input or default value
del_x = input("Width of the Gaussian in position (default is 20/p): ")
if del_x == '':
    del_x = 20/p0
else:
    del_x = float(del_x)

Ntrajs = float(input("Number of initial conditions to generate: "))

# The option to choose the distribution for the random variables
xp_dist = input("Distribution to choose the positions and momenta (uniform or normal, default uniform): ")
if xp_dist == '':
    xp_dist = 'uniform'
elif xp_dist != 'uniform' and xp_dist != 'normal':
    print('Please one of the possible probability distribution to choose positions and momenta')
    os._exit(0)

# Choice of random seed for reproducibility
random_seed = input("Define integer to use as seed for random number generation? (default uses system time): " )
if not random_seed == '':
    random_seed = int(random_seed)
    np.random.seed(random_seed)

del_p = hbar / (2.0 * del_x)

print('')
print('x0 =', x0, ' '*10, 'p0 =', p0, ' '*10, 'mass =', nuclear_mass*amu_to_au)
print('del_x =', del_x, ' '*10, 'del_p =', del_p)
print('')

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
def rejection_sampling(Ntraj, x0,p0, del_x,del_p, scale, xp_dist):
    pos_accept = []
    mom_accept = []
    pos_reject = []
    mom_reject = []

    i = 0
    while i < Ntraj:
        if xp_dist == 'uniform':
            r1 = np.random.uniform(x0 - 4.0*del_x, x0 + 4.0*del_x)
            r2 = np.random.uniform(p0 - 4.0*del_p, p0 + 4.0*del_p)
        elif xp_dist == 'normal':
            r1 = np.random.normal(x0, del_x)
            r2 = np.random.normal(p0, del_p)

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
def write_initial_conditions(pos_accepted, mom_accepted, mass):
    for i in range(len(pos_accepted)):
        os.makedirs('TRAJECTORIES/TRAJ'+str(i+1), exist_ok=True)

        with open('TRAJECTORIES/TRAJ'+str(i+1)+'/geom.orig', mode='w') as f:
            f.write('H \t 1.0 \t {:>9.6f} \t 0.000000 \t 0.000000 \t {:>14.11f} \n'.format(pos_accepted[i], mass))
        with open('TRAJECTORIES/TRAJ'+str(i+1)+'/veloc.orig', mode='w') as f:
            f.write('\t {:>14.11f} \t 0.000000 \t 0.000000 \n'.format(mom_accepted[i]/mass/amu_to_au))
    return

###############################################################################

# Grid construction
xgrid = np.arange(x0-10*del_x,x0+10*del_x,0.1)          ## I was getting the center of the initial conditinos escaping this range, when using pos=-8
pgrid = np.arange(p0-10*del_p, p0+10*del_p, 0.1)        ## then I changed so that the center is around the user given conditions
# xgrid = np.arange(-6.0,6.1,0.1)
# pgrid = np.arange(0.0, 60.1, 0.5)

print('')
print(len(xgrid), len(pgrid))
print('')
###

# Plotting the Wigner Function
P, X = np.meshgrid(pgrid, xgrid)                       ## here the shape of X and P was contrary to the shape of the envelope, which returned problems when plotting
                                                       ## I changed the order of X and P in the input and out, so they are agreeing in shape and X is still position, P is still momentum
WDF = np.array(Wigner(X,P, x0,p0,del_x,del_p))

fig = plt.figure()
ax = plt.axes(projection='3d')
surf = ax.plot_surface(X, P, WDF, rstride=1, cstride=1, cmap=cm.coolwarm,
    linewidth=0.1, antialiased=False)
#ax.set_zlim(0, 0.3)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.view_init(30, 320)
#fig.colorbar(surf, shrink=0.2, aspect=10)
plt.title('WDF')
plt.savefig('fig-wdf.png', dpi=200, bbox_inches='tight')
#plt.show()
###

# Plotting the Envelope function with WDF
Envl = np.zeros((len(xgrid), len(pgrid)))

for i in range(len(xgrid)): 
    for j in range(len(pgrid)): 
        var1 = xgrid[i]
        var2 = pgrid[j]
        Envl[i][j] = envelope(var1, var2, x0,p0,del_x,del_p) 
        
scale = np.max(WDF) / np.max(Envl)
        
fig = plt.figure()
ax = plt.axes(projection='3d')
surf1 = ax.plot_surface(X, P, WDF, cmap='cool')
surf2 = ax.plot_wireframe(X, P, scale*Envl, rstride=6, cstride=6)
ax.view_init(30, -30)
plt.savefig('fig-envelope_wdf.png', dpi=200, bbox_inches='tight')
###

# Rejection Sampling 
#Niter = 50000
pos_accept, mom_accept, pos_reject, mom_reject = rejection_sampling(Ntrajs, x0, p0, del_x, del_p, scale, xp_dist)

write_initial_conditions(pos_accept, mom_accept, nuclear_mass)

                                            ## changed the print to be more verbose and change the acceptance score calculation when using Ntrajs
print('')
print('Amount of accepted trajectories:')
print('positions: {} and momenta: {}'.format(len(pos_accept), len(mom_accept)))
print('Amount of rejected trajectories:')
print('positions: {} and momenta: {}'.format(len(pos_reject), len(mom_reject)))
print('')
print("Acceptance Score (%) =", len(pos_accept)/(len(pos_accept)+len(pos_reject))*100)
print('')


# initial condition plot
fig, ax = plt.subplots(figsize =(8, 6))
plt.hist2d(pos_accept, mom_accept, bins =[25, 25], cmap = plt.cm.nipy_spectral)
plt.colorbar()
ax.set_xlabel('position') 
ax.set_ylabel('momentum') 
plt.savefig('fig-sampling.png', dpi=200, bbox_inches='tight')
