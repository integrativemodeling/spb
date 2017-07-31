#!/bin/bash

# Exit immediately on error
set -e

# working directory
dir=$(pwd)
# file with density maps colors
file=$(dirname $0)/names_colors

if [ $# -ne 1 ]; then
  echo "Usage: $0 levels-file"
  echo
  echo "levels-file is usually HM.dat, in the same directory as the *.dx files"
  exit 1
fi

# file with density maps level value
levels=$1

nlines=$(wc -l < ${file})

# remove old chimera file
rm -f chimera_density_command_lines.txt

for i in $(seq 1 ${nlines})
do
 # extract i-th line
 riga=`sed -n ${i}p ${file}`
 # get full path to density file
 name=`echo $riga | awk '{printf "%s/%s.dx\n",dir,$1}' dir=$dir`
 # get colors
 r=`echo $riga | awk '{print $2}'`
 g=`echo $riga | awk '{print $3}'`
 b=`echo $riga | awk '{print $4}'`
 # find level value
 prefix=`echo $riga | awk '{print $1}'`
 l=`awk '{if($1==name) print $2}' name=$prefix $levels`
 # add to chimera
 echo "open $name" >> chimera_density_command_lines.txt
 echo "volume #${i} style surface level $l color ${r},${g},${b}" >> chimera_density_command_lines.txt
done

# now add visualization stuff
echo "vol all show" >> chimera_density_command_lines.txt
echo "window" >> chimera_density_command_lines.txt

echo "Chimera command file created, as chimera_density_command_lines.txt"
echo "Load the top-scoring model RMF into Chimera and then the above file"
echo "(as a Chimera commands file) to visualize the densities."
