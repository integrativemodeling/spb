#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  echo "Usage: $0 cluster_number"
  exit 1
fi

CLUSTER=$1

awk -v cl="$CLUSTER" '$2==cl {print $1,$4}' ../CLUSTER/cluster_traj_score_weight.dat > id.weight.cluster
echo "id.weight.cluster generated for cluster $CLUSTER"
