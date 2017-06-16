
imp_dir=$1

# IMP stuff
IMP=$imp_dir/setup_environment.sh
CLUSTER=$imp_dir//module_bin/membrane/spb_cluster

# get the weight.dat file from reweighting using EM2D score
rm weight.dat; for i in `seq 0 999`; do awk '{print $16}' ../ANALYSIS/frame_$i/log.dat >> weight.dat ; done

# do clustering 
$IMP $CLUSTER
