#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def read_qdct_nx_dens(inp_file):
    with open(inp_file, 'r') as f:
        lines = f.readlines()

        # list of x values
        # list of times
        # 2d array with the density
        dens_df = pd.DataFrame()
        x = []
        y = []
        for line in lines:
            if line.strip() == '':
                dens_df = pd.concat([dens_df, pd.DataFrame({np.round(time, 2): y}, index=np.round(x, 2))], axis=1)
                x = []
                y = []
                continue
            
            elif line.split()[0] == 'time:':
                time = float(line.split()[1])
                continue
            
            x.append(float(line.split()[0]))
            y.append(float(line.split()[1]))

    return dens_df.sort_index()


def read_mctdh_dens(inp_file):
    with open(inp_file, 'r') as f:
        lines = f.readlines()

        # list of x values
        # list of times
        # 2d array with the density
        dens_df = pd.DataFrame()
        x = []
        y = []
        time = 0.00
        state = 1
        for line in lines:
            if line.strip() == '':
                if state == 1:
                    tmp_y = y
                    state = 2
                    x = []
                    y = []
                    continue
                elif state == 2:
                    y = np.array(y) + np.array(tmp_y)
                    dens_df = pd.concat([dens_df, pd.DataFrame({np.round(time, 2): y}, index=np.round(x, 2))], axis=1)
                    time += 0.1
                    state = 1
                    x = []
                    y = []
                    continue
            
            x.append(float(line.split()[0]))
            y.append(float(line.split()[1]))

    return dens_df.sort_index()


if __name__ == '__main__':
	qdct_dens_df = read_qdct_nx_dens('qdct_dens.dat')
	nx_dens_df = read_qdct_nx_dens('nx_dens.dat')
	mctdh_dens_df = read_mctdh_dens('mctdh_dens.dat')


	
# plt.plot(qdct_dens_df[time], label='qdct')
# plt.plot(nx_dens_df[time].dropna(),  label='nx')
# plt.plot(mctdh_dens_df[time], label='mctdh')

# plt.legend()