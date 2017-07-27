#!/bin/bash

LAST_TIMESTEP=$(grep TimeStep log0|tail -1|awk '{print $2}')
biasIndex=$(awk "\$2==${LAST_TIMESTEP} && \$3==\"REM_Index\" && \$4==0 {print substr(FILENAME, 4)}" log*)

echo "Bias file is BIAS$biasIndex; copied to file BIAS"

cp BIAS$biasIndex BIAS

