#!/bin/bash

# run this in the parent directory (where the SAMPLING, ANALYSIS etc directories are located)
PARENT_DIR=`pwd`
SAMPLE_DIR=${PARENT_DIR}/SAMPLING
ANALYSIS_DIR=${PARENT_DIR}/ANALYSIS

for ln in `seq 0 999`
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
	rmf_slice ${SAMPLE_DIR}/traj${id}.rmf    ./RMF/frame_${i}.rmf    -f $frame
	rmf_slice ${SAMPLE_DIR}/trajisd${id}.rmf ./RMF/frameisd_${i}.rmf -f $frame

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
	
	# do analysis for this frame
	spb_analysis

	# clean
	rm *.pdb config.ini BIAS fret_new_exp.dat fret_2014.dat *.tiff frame.rmf frameisd.rmf

done
