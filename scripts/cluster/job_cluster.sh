#!/bin/bash
#$ -S /bin/bash
#$ -N second_one29_c42xtal_dist29CLUSTER 
#$ -o /scrapp/shruthi/spb/OUT_ERR 
#$ -e /scrapp/shruthi/spb/OUT_ERR
#$ -r n
#$ -j n
#$ -l netapp=10G
#$ -l h_rt=72:00:00
#$ -l mem_free=8G
#$ -l arch=linux-x64
#$ -l hostname="iq10[2-9]|iq1[1-9][0-9]|ih*|io*"
#$ -q lab.q
#$ -R yes
#$ -cwd

# load MPI and Sali modules
module load openmpi-x86_64
module load sali-libraries

# get the weight.dat file from reweighting using EM2D score
rm weight.dat; for i in `seq 0 23999`; do awk '{print $16}' ../ANALYSIS/frame_$i/log.dat >> weight.dat ; done

# IMP stuff
export IMP=/netapp/sali/shruthi/spb/code/spb-one29-distc42_dist29/build/setup_environment.sh
export CLUSTER=/netapp/sali/shruthi/spb/code/spb-one29-distc42_dist29/build/module_bin/membrane/spb_cluster

# do clustering 
$IMP $CLUSTER
