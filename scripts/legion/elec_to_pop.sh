#!/bin/bash

# Input and output file names
input_file="elec_pop.dat"
output_file="populations.dat"

# Add the header lines to the output file
echo "# Created with Newton-X version v3.5.1-40-g842842a" > "$output_file"
echo "#     Time                Step             State 1             State 2" >> "$output_file"

# Process the input file
awk '
BEGIN {
    step = 0
}
NR > 1 {
    time = $1
    state1 = $2
    state2 = $3
    printf "      %.3f                   %d      %.12f      %.12f\n", time, step, state1, state2
    step++
}
' "$input_file" >> "$output_file"

