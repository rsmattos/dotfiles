#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

amu_to_au = 1822.8885150
au_to_cminv = 219474.63068

geom = pd.read_csv('geom', sep='\s+', names=['name', 'mass', 'x', 'y', 'z', 'elec'])

veloc = pd.read_csv('veloc', sep='\s+', names=['x', 'y', 'z'])

params = pd.read_csv('newfreq_coup.txt', sep='\s+', names=['freq', 'coup'])
freq = params['freq']/au_to_cminv
coup = params['coup']


# position distribution
plt.hist(geom['x'], bins=4, alpha=0.6, edgecolor='b')
plt.legend('initial position distribution')
plt.savefig('positions.png')
plt.close()

# # position distribution
plt.hist(veloc['x'], bins=4, alpha=0.6, edgecolor='b')
plt.legend('initial velocity distribution')
plt.savefig('velocities.png')
plt.close()

# initial energies
E0 = 0.02
diacoup = 0.001

Mass = 1*amu_to_au

eta = E0 + np.dot(coup, geom['x'])
Afac = 0.5*Mass*np.dot(freq**2, geom['x']**2)
Cfac = eta**2 + diacoup**2

PE1 = Afac - np.sqrt(Cfac)
PE2 = Afac + np.sqrt(Cfac)
KE = 0.5*Mass*np.dot(veloc['x'],veloc['x'])

Etot = KE + PE1

with open('energies.txt', mode='w') as f:
	f.write('Total energy \t kinetic energy \t S0 \t S1 \n')
	f.write('{total} \t {kinetic} \t {S0} \t {S1}'
     .format(total=Etot, kinetic=KE, S0=PE1, S1=PE2))