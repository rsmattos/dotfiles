from random import random
import sys
import os

def scaled_random(min, max):
	rand = random()

	return min + rand*( max - min )

def create_traj_dir(path):
	try:
		os.mkdir(path)
	except:
		print("directory ", path, " already exists")

	return

def create_vel(path, velx):
    write_to = path + "/veloc"
    original_stdout = sys.stdout

    with open(write_to, 'w') as f:
        sys.stdout = f
        
        print("    ", velx, "    0.000000    0.00000")
    
        sys.stdout = original_stdout

def create_pos(path ,posx):
    write_to = path + "/geom"
    
    original_stdout = sys.stdout

    with open(write_to, 'w') as f:
        sys.stdout = f
        
        print(" H     1.0   ", posx, "    0.00000000    0.00000000    1.09716000")
    
        sys.stdout = original_stdout

def create_dyn(path, tmax):
    write_to = path + "/control.dyn"
    original_stdout = sys.stdout

    with open(write_to, 'w') as f:
        sys.stdout = f
        
        print(" &input")
        print("    nat        = 1")
        print("    nstat      = 2")
        print("    nstatdyn   = 2")
        print("    istep      = 0")
        print("    dt         = 0.5")
        print("    t          = 0")
        print("    tmax       =", tmax)
        print("    prog       = 0")
        print("    thres      = 100")
        print("    killstat   = 1")
        print("    timekill   = 0")
        print("    ndamp      = 0")
        print("    lvprt      = 1")
        print("    kt         = 1")
        print("    mem        = 200")
        print("    etot_jump  = 0.5")
        print("    etot_drift = 0.5")
        print("    nxrestart  = 0")
        print("/")

        sys.stdout = original_stdout    

parent = "."

for i in range(1, 21):
    posx = scaled_random(-11, -9)
    momx = scaled_random(29, 31)
    velx = momx / 1836
    tmax = int( (20 / velx)*0.024188843 + 1)

    traj = "TRAJ" + str(i)
    path = os.path.join(parent, traj)
    
    create_traj_dir(path)
    create_pos(path, posx)
    create_vel(path, velx)
    create_dyn(path, tmax)
    