#!/bin/bash
#$ -S /bin/bash
#$ -N second_one29_c42xtal_dist29ANALYSIS
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

#can reparallelize as needed
# each job id j runs for lines 40*j + 1 (j numbering from 0, lines numbering from 1)

# load MPI and Sali modules
module load openmpi-x86_64
module load sali-libraries

# IMP stuff
IMP=/netapp/sali/shruthi/imp/build/setup_environment.sh
SLICE=/netapp/sali/shruthi/imp/build/bin/rmf_slice
ANAL=/netapp/sali/shruthi/imp/build/module_bin/membrane/spb_analysis

# parent dir (where the SAMPLING, ANALYSIS etc directories are located)
PARENT_DIR=/scrapp/shruthi/spb
# data dir (where sampling was run)
SAMPLE_DIR=${PARENT_DIR}/SAMPLING/
# analysis dir
ANALYSIS_DIR=${PARENT_DIR}/ANALYSIS/ 

# zero-based numbering
j=$(( $SGE_TASK_ID - 1 ))

start_job=`echo $j | awk '{print $1*40+1}'`

end_job=`echo $start_job | awk '{print $1+39}'`

for ln in `seq $start_job $end_job`
do 
	cd $PARENT_DIR
	
	i=`echo $ln | awk '{print $1-1}'` # i is just ln index - 1

	# 1) extract rmf with single frame and store it in RMF directory
	# get info about the i-th frame
	riga=`sed -n ${ln}p ${SAMPLE_DIR}/Index_Replica0`
	# file id, i.e. log[0-7]
	id=`echo $riga    | awk '{print $4}' | cut -dg -f2`
	# frame id
	frame=`echo $riga | awk '{print $2/5}'`

	# slice from global rmf 
	$IMP $SLICE ${SAMPLE_DIR}/traj${id}.rmf    ./RMF/frame_${i}.rmf    -f $frame
	$IMP $SLICE ${SAMPLE_DIR}/trajisd${id}.rmf ./RMF/frameisd_${i}.rmf -f $frame

	# 2) run spb_analysis
	cd ANALYSIS
	# create working directory
	mkdir frame_${i}
	# go there
	cd frame_${i}
	# link file needed from ../DATA
	ln -s ../DATA/*.pdb .
	ln -s ../DATA/config.ini .
	ln -s ../DATA/fret*.dat .
	ln -s ../DATA/*.tiff .
	ln -s ../DATA/BIAS .
	ln -s ../../RMF/frame_${i}.rmf     ./frame.rmf
	ln -s ../../RMF/frameisd_${i}.rmf  ./frameisd.rmf
	# do analysis
	$IMPANAL $ANAL

	# clean
	rm *.pdb config.ini BIAS fret_new_exp.dat fret_2014.dat *.tiff frame.rmf frameisd.rmf

done
