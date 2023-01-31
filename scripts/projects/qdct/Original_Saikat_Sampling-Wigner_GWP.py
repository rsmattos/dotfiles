import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [8, 6]
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.stats as st
from scipy.interpolate import griddata
from scipy.stats import multivariate_normal
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

x0 = float(input("Initial position: "))
p0 = float(input("Initial momentum: "))
del_x = float(input("Width of the Gaussian in position: "))
del_p = hbar / (2.0 * del_x)

print('')
print('x0 =', x0, ' '*10, 'p0 =', p0)
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

def rejection_sampling(Niter, x0,p0, del_x,del_p):
    pos_accept = []
    mom_accept = []
    pos_reject = []
    mom_reject = []

    for i in range(Niter):
        r1 = np.random.normal(x0, del_x)
        r2 = np.random.normal(p0, del_p)
        u = np.random.uniform(0, scale*envelope(r1, r2, x0,p0, del_x,del_p))

        if u < Wigner(r1, r2, x0,p0,del_x,del_p):
            pos_accept.append(r1)
            mom_accept.append(r2)
        else:
            pos_reject.append(r1)
            mom_reject.append(r2)

    return np.array(pos_accept), np.array(mom_accept), np.array(pos_reject), np.array(mom_reject)
###############################################################################

# Grid construction
xgrid = np.arange(-6.0,6.1,0.1)
pgrid = np.arange(0.0, 60.1, 0.5)

print('')
print(len(xgrid), len(pgrid))
print('')
###

# Plotting the Wigner Function
X, P = np.meshgrid(xgrid, pgrid)
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
Niter = 50000
pos_accept, mom_accept, pos_reject, mom_reject = rejection_sampling(Niter, x0, p0, del_x, del_p)

print(len(pos_accept), len(mom_accept))
print(len(pos_reject), len(mom_reject))
print('')
print("Acceptance Score (%) =", len(pos_accept)/Niter*100)
print('')


# initial condition plot
fig, ax = plt.subplots(figsize =(8, 6))
plt.hist2d(pos_accept, mom_accept, bins =[25, 25], cmap = plt.cm.nipy_spectral)
plt.colorbar()
ax.set_xlabel('position') 
ax.set_ylabel('momentum') 
plt.savefig('fig-sampling.png', dpi=200, bbox_inches='tight')

