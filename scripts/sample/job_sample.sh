#!/bin/bash
#$ -S /bin/bash
#$ -N spb_SAMPLE 
#$ -o /scrapp/shruthi/spb/OUT_ERR 
#$ -e /scrapp/shruthi/spb/OUT_ERR
#$ -r n
#$ -j n
#$ -l netapp=10G
#$ -l h_rt=72:00:00
#$ -l mem_free=2G
#$ -l arch=linux-x64
#$ -R yes
#$ -cwd
#$ -t 1-600

# load MPI and Sali modules
module load openmpi-x86_64
module load sali-libraries

# IMP stuff
IMP=/netapp/sali/shruthi/imp/build/setup_environment.sh
SAMPLE=/netapp/sali/shruthi/imp/build/module_bin/spb/spb

mpirun -np 8 $IMP $SAMPLE 

