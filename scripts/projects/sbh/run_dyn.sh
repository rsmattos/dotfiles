rm sim.*
rm working.hdf5
./start.py > pyspawn.log 2>&1
./analysis.py
