#!/usr/bin/bash

grep -H Temperature log* | awk '$4==1.0 {print $1,$2,"File"}' | awk -F ':' '{print $2,$1}' > Index_Replica0

