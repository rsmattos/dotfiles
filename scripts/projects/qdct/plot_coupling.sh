#!/usr/bin/env bash

cat <<EOF > coupling.plot
set terminal pngcairo size 600,500 enhanced font "Helvetica,16"
set output 'coupling.png'
set title 'coupling'
plot 'coupling.dat' u 0:1
EOF

gnuplot coupling.plot
