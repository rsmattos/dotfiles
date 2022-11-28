#!/bin/bash

cwd=$(pwd)
input_file=~SCRIPTS/submission/inpdir

if [ $# -eq 2 ]
then
    printf '%s\n%s\n' "$1" "$(cat $input_file)" > $input_file
    printf '%s\n%s\n' "$cwd" "$(cat $input_file)" > $input_file
else
    echo "$cwd" >> $input_file
    echo "$1" >> $input_file
fi


