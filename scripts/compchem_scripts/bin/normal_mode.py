#! /usr/bin/env python3

import argparse
import os

import universe

parser = argparse.ArgumentParser(description='''\
Script to extract the normal modes from a frequency calculation output
and return it in one file for each mode or as a xyz trajectory file.''')
parser.add_argument('input',
        help="Output file with the normal mode displacement.",
        type=str
        )
parser.add_argument('--output',
        help="Name of the output file.",
        type=str,
        default='out'
        )
parser.add_argument('--trajectory',
        help="Return a trajectory file for each mode.",
        type=bool,
        nargs='?',
        const=False,
        default=True
        )
parser.add_argument('--scan',
        help="Generate one geometry for each step of each mode.",
        type=bool,
        nargs='?',
        const=True,
        default=False
        )
parser.add_argument('--steps', 
        help="Number of frames in each directions used.",
        type=int,
        default=5
        )
parser.add_argument('--modes',
        help="List of normal modes to be taken.",
        nargs='+',
        type=int
        )
args=parser.parse_args()


def read_eq_coord(file_name):
    ''' Documentation '''
    with open(file_name, 'r' ) as file:
        inp=file.readlines()

    for lineN in range(len(inp)):
        molecule=[]
        if "atomic coordinates" in inp[lineN]:
            count=1
            while (inp[lineN+count][:-1] != " "):
                line=inp[lineN+count][:-1].split()

                atom=universe.atom(name = line[3],
                                    x = line[0],
                                    y = line[1],
                                    z = line[2])

                molecule.append(atom)
                count+=1
            break
    return molecule


def read_displacements(file_name, molecule):
    ''' Documentation '''
    with open(file_name, 'r' ) as file:
        inp=file.readlines()

    for lineN in range(len(inp)):
        if "NORMAL MODES and VIBRATIONAL FREQUENCIES" in inp[lineN]:
            count=12 #skipping the frequencies documentation
            while (not "time elapsed for vibrational analysis" in inp[lineN+count][:-1]):
                if "RAMAN" in inp[lineN+count][:-1]:
                    count+=2 #Jumping the empty line before the RAMAN statement
                    for atom in molecule:
                        line = inp[lineN+count][:-1].split()
                        for disp in range(3,len(line)):
                            atom.set_Dx(line[disp])
                        count+=1
                        
                        line = inp[lineN+count][:-1].split()
                        for disp in range(1,len(line)):
                            atom.set_Dy(line[disp])
                        count+=1
                        
                        line = inp[lineN+count][:-1].split()
                        for disp in range(1,len(line)):
                            atom.set_Dz(line[disp])
                        count+=1

                count+=1
                line=inp[lineN+count][:-1].split()
    return None


def calc_modes(molecule, nsteps, mode):
    """ Receives one normal mode index and generates the displaced
    coordinates for this mode.
    """
    
    displaced = []

    for step in range(-nsteps,nsteps+1):
        stepName="{0:0>2}_step".format(step)
        create_dir("{0}/{1}/{2}".format(input_name, dispName, stepName))
        out = open("{0}/{1}/{2}/coord".format(input_name, dispName, stepName),'w')
        out.write("$coord\n")
        for atom in molecule:
            xCoord=float(atom.get_x()) + float(atom.get_Dx()[dispCount])*(step/nsteps)
            yCoord=float(atom.get_y()) + float(atom.get_Dy()[dispCount])*(step/nsteps)
            zCoord=float(atom.get_z()) + float(atom.get_Dz()[dispCount])*(step/nsteps)
            out.write("{1: 18.9f} {2: 18.9f} {3: 18.9f} {0:>5s}\n".format(atom.get_name(),
                                                float(xCoord),
                                                float(yCoord),
                                                float(zCoord)))
        out.write("$end\n")
        out.close()

    return displaced


if __name__ == "__main__":
    if not os.path.isfile(args.input):
        print("Check your input file name!!\n")
        exit()

    molecule = read_eq_coord(args.input)
    print("{0} atoms computed.".format(len(molecule)))

    read_displacements(args.input,molecule)
    print("{0} frequencies evaluated.".format(len(molecule[2].get_Dx())))

    print(molecule[0].get_Dx())

