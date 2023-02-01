#!/usr/bin/env python3

import pandas as pd

def help_function(script_name):
    description = """
    ###################################################################################
    # script to print to screen the electronic population in the properties file      #
    #                                                                                 #
    # input: properties.hdf5														  #
    #                                                                                 #
    # output: print the population to screen                                          #
    #                                                                                 #
    # calling: {}
    ###################################################################################
    """.format(script_name)
    print(description)
    os._exit(0)

def print_population():
	pop = pd.read_hdf('properties.hdf5', mode='r', key='elec_pop').iloc[-1]['S0']

	print(pop)	

if __name__ == '__main__':
    if str(sys.argv[1]) == '-h':
        help_function(sys.argv[0])

    print_population()
