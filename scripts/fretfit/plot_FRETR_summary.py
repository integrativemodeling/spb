#!/usr/bin/env python

from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import time
import sys
import matplotlib.mlab as mlab
import math
import random

# cluster_id
CL_ID_=int(sys.argv[1])
# weight file
WEIGHT_FILE_=sys.argv[2]
# ANALYSIS directory
ANAL_DIR_=sys.argv[3]
# data file
DATA_FILE_=sys.argv[4]
# output file suffix
OUTFILE_SUFFIX_=sys.argv[5]

# read weights
ww=[]; ids=[]

for line in open(WEIGHT_FILE_,'r').readlines():
    riga=line.strip().split()
    if(len(riga)!=5): continue
    # check if right cluster
    if(int(riga[1])!=CL_ID_): continue
    ww.append(float(riga[3]))
    ids.append(int(riga[0]))

# read data file, with fret pairs, fexp, and fexp_err
data={}
data["name"]=[]; data["fexp"]=[]; data["fexp_err"]=[]

for line in open(DATA_FILE_,'r').readlines():
    riga=line.strip().split()
    if(len(riga)!=4): continue
    data["name"].append((riga[0],riga[1]))
    data["fexp"].append(float(riga[2]))
    data["fexp_err"].append(float(riga[3]))

# read model data
fmod={}
# initialize dictionary of lists
for pair in data["name"]:
    fmod[pair]=0.0
    
# first normalize the weights to sum to 1
sum_ww=0.0
for wt in ww:
  sum_ww=sum_ww+wt

for i in range(len(ww)):
  ww[i]=ww[i]/sum_ww

# cycle on cluster members 
for id,weight in zip(ids,ww):
 # open fret.dat file 
 for line in open(ANAL_DIR_+"/frame_"+str(id)+"/fret.dat",'r').readlines():
     riga=line.strip().split()
     if(riga[2]!="Name"): continue
     pair=(riga[3],riga[4])
     fmod[pair]=fmod[pair]+float(riga[6])*weight 


xvals=[i+1 for i in range(len(fmod))]
yvals=[fmod[pair] for pair in data["name"]]

for pair,i in zip(data["name"],range(len(data["name"]))):
    #print(pair, fmod[pair], data["fexp"][i], data["fexp_err"][i])
    print(pair[0],pair[1], "%.4f" %(fmod[pair]) , data["fexp"][i], data["fexp_err"][i])

# plot experimental value with error
plt.figure()
exptPlot= plt.errorbar(xvals,data["fexp"],yerr=data["fexp_err"],fmt='-o',color="red",linewidth=1) # experimental values with error bars

modelPlot=plt.errorbar(xvals,yvals,yerr=0.02,fmt='-o',color="black",linewidth=1) # model values

plt.xlabel("Protein pair")
plt.ylabel("FRET$_R$")

if OUTFILE_SUFFIX_=="MERGED_RUNS_CLUSTER_WITHOUT_SPC29":
    plt.legend([exptPlot,modelPlot],["Experiment","Model (1x Spc29)"])
elif OUTFILE_SUFFIX_=="TWOCOPIESSPC29_CLUSTER_WITH_SPC29": 
    plt.legend([exptPlot,modelPlot],["Experiment","Model (2x Spc29)"])
else:
    plt.legend([exptPlot,modelPlot],["Experiment","Model"])

OUTFILE_SUFFIX_=OUTFILE_SUFFIX_+"_cluster"+str(CL_ID_)
plt.savefig("fretsummary_"+OUTFILE_SUFFIX_+".pdf",dpi=600)

#plt.show()
