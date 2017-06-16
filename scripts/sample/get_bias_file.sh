#!/bin/bash

biasIndex=`seq 0 7 | xargs -i awk '$2==119995 && $3=="REM_Index" {print}' log{} | awk '$4==0 {print NR-1}'`

cp BIAS$biasIndex BIAS

