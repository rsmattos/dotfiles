#!/usr/bin/env python3

import numpy as np
import sys

def convert(data, conversion):
    return data*conversion


def read_xyz(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    n_atoms = int(lines[0])
    title = lines[1]

    atom_list = []
    positions = np.zeros(shape=(n_atoms, 3))

    for idx, line in enumerate(lines[2:]):
        words = line.split()
        atom_list.append(words[0])

        positions[idx, 0] = float(words[1])
        positions[idx, 1] = float(words[2])
        positions[idx, 2] = float(words[3])

    return title, atom_list, positions


def write_xyz(filename, title, atom_list, positions):
    txt = f'{len(atom_list)}\n'
    txt += f'{title}'

    for atom, pos in zip(atom_list, positions):
        txt += f'{atom} \t {pos[0]} \t {pos[1]} \t {pos[2]}\n'
    
    with open(filename, 'w') as f:
        f.write(txt[:-1])

    return


if __name__ == '__main__':
    BOHR2ANG = 0.529177249

    filename = sys.argv[1]
    print(filename)

    title, atom_list, positions = read_xyz(filename)
    positions = convert(positions, BOHR2ANG)
    write_xyz(filename, title, atom_list, positions)
