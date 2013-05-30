#!/bin/bash


for i in {1..$4}; 
do 
    time python $1 $2 $3; 
done 2>&1 | grep ^user | sed -e s/.*m// | awk '{sum += $1} END {print sum / NR}'