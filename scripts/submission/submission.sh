#!/bin/bash

sub_root="$( dirname -- "$0"; )"

function update_inpdir
{
    n_lines=$(wc -l $sub_root/inpdir | awk '{print $1}')
#    echo "$n_lines"

    dir_atual=$(head -n 1 $sub_root/inpdir)
    order=$(head -n 2 $sub_root/inpdir | tail -n 1)
#    echo "dir_atual $dir_atual"
#    echo "order $order"
    tail -n +3 $sub_root/inpdir > $sub_root/inpdir.tmp && mv $sub_root/inpdir.tmp $sub_root/inpdir
}

function running_jobs
{
    limit=$(head -n 1 $sub_root/job_limit)
#    echo "limit $limit"
    lines=$(ls -lh $sub_root/submitted | wc -l)
    n_jobs=$(($lines - 1))
#    echo "n of jobs $n_jobs"
}

function update_log
{
    echo "" >> $sub_root/log_file
    echo $dir_atual >> $sub_root/log_file
    echo $sub_file >> $sub_root/log_file
}

update_inpdir
running_jobs

# BEGIN SCRIPT

while [ $n_lines -gt 0 ]
do
    a=0
    while [ $a -lt 1 ]
    do
        if [ $n_jobs -lt $limit ]
        then
#            echo "creating submission file"
            sub_file=$(date +"%FT%T")_$RANDOM
            echo "cd $dir_atual" > $sub_root/submitted/$sub_file
            echo "$order" >> $sub_root/submitted/$sub_file
            echo "rm $sub_root/submitted/$sub_file" >> $sub_root/submitted/$sub_file
#            echo "running submission file"
            bash $sub_root/submitted/$sub_file &
            update_log
            a=2
            sleep 0.1
        else
            sleep 2
        fi
        running_jobs
    done
    update_inpdir
done

