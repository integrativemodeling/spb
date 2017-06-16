#!/bin/bash
imp_dir=$1
date
 mpirun -np 8 $imp_dir'/build/setup_environment.sh' $imp_dir'/build/module_bin/spb/spb'
date
