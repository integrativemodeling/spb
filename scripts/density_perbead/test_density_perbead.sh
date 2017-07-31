#!/bin/bash

# Exit immediately on error
set -e
imp_dir=$1

cluster_number=0

# get the file lista_frames.dat 
cat ../CLUSTER/cluster_traj_score_weight.dat | awk -v cn="$cluster_number" '$2==cn {print $1,$4}' | sort -n -r -k 2 | awk '{print "../RMF/frame_"$1".rmf","../RMF/frameisd_"$1".rmf",$2}' > lista_frames.dat

refRmf=$(head -n 1 lista_frames.dat | awk '{print $1}')
refIsdRmf=$(head -n 1 lista_frames.dat | awk '{print $2}')

# modify the config.ini file to add the lines corresponding to reference frame (first model in the cluster i.e. first line of lista_frames.dat
if grep ^map_ref_file config.ini >/dev/null
then
  echo "Already have ref RMF"
else
  echo "map_ref_file="$refRmf >> config.ini
  echo "map_ref_isdfile="$refIsdRmf >> config.ini
fi

spb_density_perbead
