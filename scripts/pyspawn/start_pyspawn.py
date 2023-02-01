#!/usr/bin/env python2

# this script starts a new FMS calculation on a model cone potential
import numpy as np
import pyspawn
import pyspawn.general
import pyspawn.process_geometry as pg

# Processing geometry file
natoms, atoms, coords, masses = pg.process_geometry('geom.orig', 'newtonX')
velocities = pg.process_velocity('veloc.orig')

momenta = velocities*masses

widths_dict = {'C': 22.0, 'H': 4.5}
widths = np.asarray([widths_dict[atom] for atom in atoms for i in range(3)])

# Velocity Verlet classical propagator
clas_prop = "vv"

# adaptive 2nd-order Runge-Kutta quantum propagator
qm_prop = "fulldiag"

# adiabatic NPI quantum Hamiltonian
qm_ham = "adiabatic"

# use TeraChem CASSCF or CASCI to compute potentials
potential = "tully_1"

# initial time
t0 = 0.0

# time step
ts = 1.

# final simulation time
tfinal = 4000.0

# number of dimensions
numdims = natoms*3

# number of electronic states
numstates = 2

# coupling type is 'nac', 'tdc' or 'vh'
coupling_type = 'nac'

# print level can be 'normal' or 'verbose'
print_level = 'normal'

# do qm propagation in pyspawn?
do_qm_propagation = True

# trajectory parameters
traj_params = {
    # initial time
    "time": t0,
    # time step
    "timestep": ts,
    # final simulation time
    "maxtime": tfinal,
    # coupling threshold
    # "spawnthresh": (0.5 * np.pi) / ts / 20.0,
    "spawnthresh": 0.008,
    # initial electronic state (indexed such that 0 is the ground state)
    "istate": 0,
    # Gaussian widths
    "widths": widths,
    # atom labels
    "atoms": atoms,
    # nuclear masses (in a.u)
    "masses": masses,
    # initial positions
    "positions": coords,
    # inition momenta
    "momenta": momenta,
}

sim_params = {
    # initial time
    "quantum_time": traj_params["time"],
    # time step
    "timestep": traj_params["timestep"],
    # final simulation time
    "max_quantum_time": traj_params["maxtime"],
    # initial qm amplitudes
    "qm_amplitudes": np.ones(1, dtype=np.complex128),
    # energy shift used in quantum propagation
    "qm_energy_shift": -0.0
}

# import routines needed for propagation
exec ("pyspawn.import_methods.into_simulation(pyspawn.qm_integrator." + qm_prop + ")")
exec ("pyspawn.import_methods.into_simulation(pyspawn.qm_hamiltonian." + qm_ham + ")")
exec ("pyspawn.import_methods.into_traj(pyspawn.potential." + potential + ")")
exec ("pyspawn.import_methods.into_traj(pyspawn.classical_integrator." + clas_prop + ")")

# check for the existence of files from a past run
pyspawn.general.check_files()

# set up first trajectory
traj1 = pyspawn.traj(numdims, numstates, coupling_type)
# traj1.set_numstates(numstates)
# traj1.set_numdims(numdims)
traj1.set_parameters(traj_params)

# set up simulation
sim = pyspawn.simulation(coupling_type)
sim.set_do_qm_propagation(do_qm_propagation)
sim.set_print_level(print_level)
sim.add_traj(traj1)
sim.set_parameters(sim_params)

# begin propagation
sim.propagate()
