#!/usr/bin/env python3

import os
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10, 6]
import scipy.stats as stats
import shutil

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Universal Constants and Conversion 
hbar = 1.
amu_to_au = 1822.8885150
cminv_to_au = 219474.63068

myfile1 = open('newenr.txt', 'w')
myfile2 = open('newcoord_mom_vel.txt', 'w')
myfile3 = open('newfreq_coup.txt', 'w')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Spin-Boson Hamiltonian Parameters

NB = 1                                 # SBH dimension
Mass = 1.0*amu_to_au                   # Mass (AMU)
E0 = 0.03                              # Energy Bias (au)
DiaCoup = 0.05                         # Diabatic Coupling (au)
WMAX = 4000.0/cminv_to_au              # Maximum Frequency (cm-1)
WC = WMAX/3.0                          # Cut-Off Frequency 
#ER = 0.0125                           # Coupling Strength in Debye Spectral Density (au)
ER = 0.0
Arg = np.arctan(WMAX/WC)

WB = np.zeros(NB)
SD = np.zeros(NB)
GB = np.zeros(NB)

R_Min = np.zeros(NB)
P_Min = np.zeros(NB)

Sigma_R = np.zeros(NB)
Sigma_P = np.zeros(NB)

zpe = 0.0
# Discretization of Frequrncy, Spin-Bath Coupling 
for i in range(NB):
    WB[i] = WC*np.tan((i+1)/NB*Arg)
    GB[i] = np.sqrt(Mass*ER/(math.pi*NB)*Arg)*WB[i]
    
    R_Min[i] = GB[i]/Mass/WB[i]**2
    P_Min[i] = np.sqrt(hbar*Mass*WB[i])
 
    Sigma_R[i] = np.sqrt(hbar/(2.*Mass*WB[i]))
    Sigma_P[i] = np.sqrt(hbar*Mass*WB[i]/2.)
    
    zpe = zpe + 0.5*hbar*WB[i]
    
    myfile3.write("{:15.10f} {:15.10f}".format(WB[i]*cminv_to_au, GB[i]))
    myfile3.write('\n')

print('ZPE =', zpe)
zpeshift = zpe - E0
print('zpeshift =', zpeshift)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Perform Sampling from a normal distribution

M = 3200                             # No. of Trajectories (init cond)

RR = np.zeros((NB, M)) 
MM = np.zeros((NB, M))
VV = np.zeros((NB, M))

np.random.seed(42)                     # Random Number Seed

mom_pos = 'correlated'
## uncorrelated momentum and position
if mom_pos == 'uncorrelated':
    for i in range(NB):
        RR[i,:] = np.random.normal(R_Min[i], Sigma_R[i], M)
        MM[i,:] = np.random.normal(0.0, Sigma_P[i], M)
        VV[i,:] = MM[i,:]/Mass

## correlated momentum and position
elif mom_pos == 'correlated':
    for i in range(NB):
        filter = hbar*WB[i]
        for j in range(M):
            check = filter + 1
            while(check > filter):
                pos = np.random.normal(R_Min[i], Sigma_R[i])
                check = Mass*WB[i]*WB[i]*pos*pos
            RR[i,j] = pos
        MM[i,:] = np.sqrt(Mass)*np.sqrt(hbar*WB[i] - Mass*WB[i]*WB[i]*RR[i,:]*RR[i,:])*\
                    (2*np.random.randint(0, 2, M)-1)
        VV[i,:] = MM[i,:]/Mass

for j in range(M):
    for i in range(NB):
        myfile2.write("{:15.10f} {:15.10f} {:15.10f}\n"
               .format(RR[i,j], MM[i,j], VV[i,j]))

    myfile2.write('#\n')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Total Energy for each initial condition 

Etot = np.zeros(M)

for j in range(M):
    
    eta =  0.0
    Afac = 0.0
    Bfac = 0.0 
    for i in range(NB):
        eta = eta + GB[i]*RR[i,j]
        Afac = Afac + 0.5*Mass*WB[i]**2*RR[i,j]**2
        Bfac = Bfac + 0.5*Mass*VV[i,j]**2
    eta = eta + E0
    Cfac = eta**2 + DiaCoup**2
    
    PE1 = Afac + (-1.0)**1*np.sqrt(Cfac)
    PE2 = Afac + (-1.0)**2*np.sqrt(Cfac)
    KE = Bfac

    Etot[j] = KE + PE1 

    myfile1.write("{:5d} {:15.10f} {:15.10f} {:15.10f} {:15.10f}".format(j, KE, PE1, PE2, Etot[j]))
    myfile1.write('\n')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

myfile1.close()
myfile2.close() 
myfile3.close() 

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Mean = np.mean(Etot)
Std = np.std(Etot)
print(Mean,Std)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

plt.figure(figsize=(8,6))
density2 = stats.gaussian_kde(Etot)
n2, x2, _ = plt.hist(Etot, bins=50, alpha=0.6, label="Total Energy (KE + PE1)", edgecolor='b')
plt.xlabel("Energy (a.u.)", size=16)
plt.ylabel("Count", size=16)
plt.xlim(-0.02,0.06)
plt.xticks(np.arange(-0.02, 0.06, step=0.01))
plt.axvline(x=zpeshift,  color='k', linestyle='--', label="ZPE")
plt.axvline(x=Mean, color='r', linestyle='--', label= "Mean value")
plt.hlines(y=60, xmin=Mean-Std, xmax=Mean+Std, linestyle='-', color='r', label ="Standard Deviation")
plt.legend(fontsize=14)
#plt.plot(x2, density2(x2), 'r-')
plt.savefig("newIC.png", dpi=600)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

llimit = zpeshift - 0.01
hlimit = zpeshift + 0.01
Elist = []
index = []
Eout = []
indexout = []

for j in range(M):
    if ((Etot[j] > llimit) and (Etot[j] < hlimit)):
        Eout.append(Etot[j])
        indexout.append(j)
    else:
        Elist.append(Etot[j])
        index.append(j)
        
newE = np.array(Elist)
print(np.shape(newE))   
print(len(index))
print(index)

outE = np.array(Eout)
print(np.shape(outE))
print(len(indexout))
print(indexout)

newmean = np.mean(newE)
newstd = np.std(newE)

print(newmean, newstd)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Rtemp = []
Vtemp = []
for j in index:
    for i in range(NB):
        Rtemp.append(RR[i,j])
        Vtemp.append(VV[i,j])
print(len(Rtemp)) 
print(len(Vtemp))

Rselect = np.asarray(Rtemp).reshape(NB, len(index), order='F')
Vselect = np.asarray(Vtemp).reshape(NB, len(index), order='F')
print(np.shape(Rselect))
print(np.shape(Vselect))

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Rtempout = []
Vtempout = []
for j in indexout:
    for i in range(NB):
        Rtempout.append(RR[i,j])
        Vtempout.append(VV[i,j])
print(len(Rtempout)) 
print(len(Vtempout))

Rout = np.array(Rtempout).reshape(NB, len(indexout), order='F')
Vout = np.array(Vtempout).reshape(NB, len(indexout), order='F')
print(np.shape(Rout))
print(np.shape(Vout))

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

plt.figure(figsize=(8,6))
plt.hist(Etot, bins=50, alpha=0.8, label="Total energy (3000 ICs)", edgecolor='b')
plt.hist(newE, bins=20, alpha=0.6, label="Total energy (2000 selected ICs)", edgecolor='r')
plt.hist(outE, bins=40, alpha=0.4, label="Total energy (out region ICs)", edgecolor='g')
plt.xlabel("Energy (a.u.)", size=16)
plt.ylabel("Count", size=16)
plt.xlim(-0.02,0.06)
plt.xticks(np.arange(-0.02, 0.06, step=0.01))
plt.axvline(x=zpeshift,  color='k', linestyle='--', label="ZPE")
plt.axvline(x=Mean, color='b', linestyle='--', label= "Mean value for 3000 ICs")
plt.axvline(x=newmean, color='r', linestyle='--', label= "Mean value for 2000 selected ICs")
#plt.hlines(y=60, xmin=newmean-newstd, xmax=newmean+newstd, linestyle='-', color='r', label ="Standard Deviation")
plt.legend(fontsize=14)
plt.savefig("selectIC.png", dpi=600)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# First Delete the existing TRAJECTORIES directory
shutil.rmtree(r'TRAJ_INSIDE')

print('will be using the index')
print(index)

os.mkdir('TRAJ_INSIDE')
#os.mkdir('TRAJ_OUTSIDE')

for j in range(len(index)):
    os.mkdir('TRAJ_INSIDE/TRAJ'+str(j+1))
#    os.system('cp user_config.nml TRAJ_INSIDE/TRAJ'+str(j+1))
#    os.system('cp -r JOB_NAD TRAJ_INSIDE/TRAJ'+str(j+1))
    os.chdir('TRAJ_INSIDE/TRAJ'+str(j+1))
    with open('geom.orig', 'w') as g, open('veloc.orig', 'w') as v:
        for i in range(NB):
            g.write("{:5} {:15.10f} {:15.10f} {:15.10f} {:15.10f} {:15.10f}".format('H', 1.0, Rselect[i,j], 0.0, 0.0, Mass/amu_to_au))
            g.write('\n')
            v.write("{:15.10f} {:15.10f} {:15.10f}".format(Vselect[i,j], 0.0, 0.0))
            v.write('\n')
    os.chdir('../../')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#for j in range(len(indexout)):
#    os.mkdir('TRAJ_OUTSIDE/TRAJ'+str(j+1))
#    os.system('cp configuration.inp TRAJ_OUTSIDE/TRAJ'+str(j+1))
#    os.system('cp -r JOB_NAD TRAJ_OUTSIDE/TRAJ'+str(j+1))
#    os.system('cp submit_nx.job TRAJ_OUTSIDE/TRAJ'+str(j+1))
#    os.chdir('TRAJ_OUTSIDE/TRAJ'+str(j+1))
#    with open('geom.orig', 'w') as g1, open('veloc.orig', 'w') as v1:
#        for i in range(NB):
#            g1.write("{:5} {:15.10f} {:15.10f} {:15.10f} {:15.10f} {:15.10f}".format('C', 1.0, Rout[i,j], 0.0, 0.0, Mass/amu_to_au))
#            g1.write('\n')
#            v1.write("{:15.10f} {:15.10f} {:15.10f}".format(Vout[i,j], 0.0, 0.0))
#            v1.write('\n')
#    os.chdir('../../')
