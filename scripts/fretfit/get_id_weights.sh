#!/bin/bash

CLUSTER=$1

awk -v cl="$CLUSTER" '$2==cl {print $1,$4}' ../CLUSTER/cluster_traj_score_weight.dat > id.weight.cluster
