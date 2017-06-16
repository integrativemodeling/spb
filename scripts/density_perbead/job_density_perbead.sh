#!/bin/bash
#$ -S /bin/bash
#$ -N second_one29_c42xtal_dist29DENSITY_PB
#$ -o /scrapp/shruthi/spb/OUT_ERR
#$ -e /scrapp/shruthi/spb/OUT_ERR
#$ -r n
#$ -j n
#$ -l netapp=10G
#$ -l h_rt=2:00:00
#$ -l mem_free=2G
#$ -l arch=linux-x64
#$ -R yes
#$ -cwd
#$ -pe ompi 64 
##$ -q lab.q

# load MPI and Sali modules
module load openmpi-1.6-nodlopen
module load sali-libraries

cluster_number=0

# get the file lista_frames.dat 
cat ../CLUSTER/cluster_traj_score_weight.dat | awk -v cn="$cluster_number" '$2==cn {print $1,$4}' | sort -n -r -k 2 | awk '{print "/scrapp/shruthi/spb/RMF/frame_"$1".rmf","/scrapp/shruthi/spb/RMF/frameisd_"$1".rmf",$2}' > lista_frames.dat

refRmf=`head -n 1 lista_frames.dat | awk '{print $1}'`
refIsdRmf=`head -n 1 lista_frames.dat | awk '{print $2}'`

# modify the config.ini file to add the lines corresponding to reference frame (first model in the cluster i.e. first line of lista_frames.dat
if grep ^map_ref_file config.ini >/dev/null
then
        echo "Already have ref RMF"
else
        echo "map_ref_file="$refRmf >> config.ini
        echo "map_ref_isdfile="$refIsdRmf >> config.ini
fi

date
# IMP stuff
export IMP=/netapp/sali/shruthi/spb/code/spb-one29-distc42_dist29/build/setup_environment.sh
export MAP=/netapp/sali/shruthi/spb/code/spb-one29-distc42_dist29/build/module_bin/membrane/spb_density_perbead

mpirun -np $NSLOTS $IMP $MAP

date
