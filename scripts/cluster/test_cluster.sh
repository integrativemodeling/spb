#!/bin/bash

# Exit immediately on error
set -e

LAST_FRAME=$(( $(ls -d ../ANALYSIS/frame_*| wc -l) - 1 ))

# get the weight.dat file from reweighting using EM2D score
rm -f weight.dat
for i in $(seq 0 $LAST_FRAME); do
  awk '{print $16}' ../ANALYSIS/frame_$i/log.dat >> weight.dat
done

# do clustering 
spb_cluster
