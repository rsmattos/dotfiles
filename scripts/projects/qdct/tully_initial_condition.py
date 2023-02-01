#!/usr/bin/env python3

############################################################
# script to generate initial positions for a NX simularion 
# around a given position for the tully models             
############################################################

import numpy as np
import random
import sys

# general values
## variables
### central positions
q = -8
min_q = -10
max_q = -6
range_q = max_q - min_q

### central momentum
p = 10

### numver of trajectories
N = int(sys.argv[1])

### widths of the nuclear wavefuncion
w = 4.5

# gaussian distribution
def gaussian_dist(x):
    c1i = complex(0., 1.)
    qdiff = x - q
    gaussian = np.exp(-w*qdiff*qdiff + c1i*p*qdiff)
    return np.real(np.vdot(gaussian, gaussian))

# loop to generate the positions
i = 0
positions = []

while i < N:
    x = min_q + range_q*random.random()
    y = random.random()

    if y < gaussian_dist(x):
        positions.append(x)
        i += 1

for i in range(len(positions)):
    with open('TRAJ'+str(i+1)+'/geom.orig', mode='w') as f:
        f.write('H \t 1.0 \t {:>9.6f} \t 0.000000 \t 0.000000 \t 1.09716000'.format(positions[i]))
