#!/usr/bin/env bash


for i in {100..1000..100}
do $SCRIPTS/mixdyn/average_elec_pop.py $i
   mv average_pop.png average_pop_$i.png
   mv populations.dat populations_$i.dat
done

$SCRIPTS/newtonX/populations.plot
