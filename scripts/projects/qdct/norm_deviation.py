#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame()

for i in range(1, 501):
	df_tmp = pd.read_csv('single_TRAJ{}_elec_pop.dat'.format(i), sep='\s+', usecols=[0, 1], index_col=[0], skiprows=1, names=['time', i])
	df = pd.concat([df, df_tmp], axis=1)

maximum_norm = df.max()
minimum_norm = df.min()
final_norm = df.iloc[-1]

print(maximum_norm)
print(minimum_norm)
print(final_norm)

plt.plot(maximum_norm, label='max')
plt.plot(minimum_norm, label='min')
plt.plot(final_norm, label='final')
plt.legend()
plt.savefig('norm_deviation')