#!/usr/bin/env python3

import sys
sys.path.append('/data/Rafael/Projects/03-QDCT/software')
import main as qdct

parameters = qdct.params('sim.hdf5')
#parameters.set_shift(-0.0)
#parameters.set_expansion_factor(2)

qdct.run_analysis(parameters)
