#!/usr/bin/env zsh

if [ ! -f './TRAJECTORIES/TRAJ1/populations.dat' ]; then
    cd TRAJECTORIES

    for d in TRAJ*
    do
        cd $d
        $SCRIPTS/legion/elec_to_pop.sh
        cd ..
    done

    cd ..
fi

for i in {100..1000..100}
do
    echo "${i}\n${1}\n0.1\n1" | $SCRIPTS/legion/bootstrap_pop
    mv BSAVG-ADIAPOP.dat BSAVG-ADIAPOP_${i}.dat
done
