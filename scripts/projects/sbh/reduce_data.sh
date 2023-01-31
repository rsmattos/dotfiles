#!/usr/bin/env bash

/data/Rafael/Projects/04-SBH/bin/extract_coefs.py \
&& /data/Rafael/Projects/04-SBH/bin/extract_elec_pop.py \
&& /data/Rafael/Projects/04-SBH/bin/extract_nuc_pop.py \
&& rm analysis.hdf5
