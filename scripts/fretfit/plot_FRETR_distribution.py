#!/usr/bin/env python

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
# data file: can combine FRET points removed and added during sampling
DATA_FILE_=sys.argv[4]
# raw data from experiment
RAW_DATA_FILE_=sys.argv[5] 
#file name ofoutput file
OUTFILE_SUFFIX_= sys.argv[6]
OUTFILE_SUFFIX_ = OUTFILE_SUFFIX_ + "_cluster_"+str(CL_ID_)


# read weights
ww_models=[]; ids=[]

for line in open(WEIGHT_FILE_,'r').readlines():
    riga=line.strip().split()
    if(len(riga)!=5): continue
    # check if right cluster
    if(int(riga[1])!=CL_ID_): continue
    ww_models.append(float(riga[3]))
    ids.append(int(riga[0]))

print "Finished reading cluster weights file."

# read data file, with fret pairs, fexp, and fexp_err
data={}
data["name"]=[]; data["fexp"]=[]; data["fexp_err"]=[]

for line in open(DATA_FILE_,'r').readlines():
    riga=line.strip().split()
    if(len(riga)!=4): continue
    data["name"].append((riga[0],riga[1]))
    data["fexp"].append(float(riga[2]))
    data["fexp_err"].append(float(riga[3]))

print "Finished reading the FRETR values used for sampling."

# read raw data
rawdatawithdate={}
wtfretrbydate={}
rawdata={}
ww_raw={}

for line in open(RAW_DATA_FILE_,'r').readlines():
    riga=line.strip().split()
    ppair=(riga[1],riga[2])
    date=riga[0]
    fretr=float(riga[3])
    
    if ppair not in rawdatawithdate: # create new list
      rawdatawithdate[ppair]=[(fretr,date)] # each entry is a tuple with raw data and date as the 2 entries
      
    else:
      rawdatawithdate[ppair].append((fretr,date))
      
    if ppair not in wtfretrbydate:
	  wtfretrbydate[ppair]={}
	  wtfretrbydate[ppair][date]=1.0 #first member, new pair, new date
    else:
	  if date not in wtfretrbydate[ppair]:
	      wtfretrbydate[ppair][date]=1.0  #first member, existing pair, new date
	  else:
	      wtfretrbydate[ppair][date]+=1.0 # exists pair and date, just increment
     
	
# get the weight of each raw data point as inverse of the population for that date, for that pair. 
for pair in rawdatawithdate: 
	rawdata[pair]=[]
	ww_raw[pair]=[]
	for fret_date in  rawdatawithdate[pair]: 
	    rawdata[pair].append(fret_date[0])
	    ww_raw[pair].append(1.0/wtfretrbydate[pair][fret_date[1]])
	    		
print "Finished reading raw experimental data"

# read model data
fmod={}
# initialize dictionary of lists
for pair in data["name"]:
    fmod[pair]=[]

#print fmod

# cycle on cluster members
dirs_to_search=[ANAL_DIR_]
if OUTFILE_SUFFIX_.startswith("NOCC"):
	dirs_to_search=[ANAL_DIR_,ANAL_REMOVED_DIR_]
#elif OUTFILE_SUFFIX_.startswith("RAND"):                             
#        dirs_to_search=[ANAL_REMOVED_DIR_]
# else default
 
for id in ids:
 for dirs in dirs_to_search:
	# open fret.dat file 
 	for line in open(dirs+"/frame_"+str(id)+"/fret.dat",'r').readlines():
     		riga=line.strip().split()
     		if(riga[2]!="Name"): continue
     		pair=(riga[3],riga[4])
     		fmod[pair].append(float(riga[6]))

 
print "Number of FRET points", len(fmod)

print "Finished reading FRETR from models"

def get_histo_models(modeldata, ws_models, xmin, xmax):
    
    '''q75, q25 = np.percentile(modeldata, [75 ,25],interpolation="lower")
    iqr = q75 - q25 #inter quartile range
   
    if iqr == 0.0:
	dx = 0.001
	 
    else: 
	#spacing
    	dx = 2.0 * iqr * (float(len(modeldata))**(-1.0/3.0))
    '''
    dx = 3.49*np.std(modeldata)*(float(len(modeldata))**(-1.0/3.0))
    if dx == 0.0:
	dx = 0.001


    nbin = int(math.ceil((xmax-xmin)/dx)) #ceil or floor??

    ## prepare stuff
    histo=[]; bincenters=[]
    
    # initialize histo
    for i in range(nbin):
        histo.append(0.0)
        #bins.append(xmin + float(i) * dx)
	bincenters.append(xmin + float(i) * dx + dx/2.0)
    
    # fill histo
    for i,d in enumerate(modeldata):
        # check if within boundaries
        if(d<xmin or d>=xmax): continue
	index = int(math.floor((d-xmin)/dx))
        histo[index] += ws_models[i]
              
    # normalize histo and gauss
    normh = sum(histo)
  
    for i in range(len(histo)):
        histo[i] /= normh
   
    #return histo, bins 
    return histo, nbin, bincenters 
    
def get_histo_raw(rawdatapair, ws_raw_pair, xmin, xmax):
    '''q75, q25 = np.percentile(rawdatapair, [75 ,25],interpolation="lower")
    iqr = q75 - q25 #inter quartile range
   
    #if iqr == 0.0:
    #	print rawdatapair, ws_raw_pair
 
    #spacing
    dx = 2.0 * iqr * (float(len(rawdatapair))**(-1.0/3.0))
    '''
    dx = 3.49 * np.std(rawdatapair) * (float(len(rawdatapair))**(-1.0/3.0))
  
    if dx == 0.0:
	dx = 0.001


    nbin = int(math.ceil((xmax-xmin)/dx)) #ceil or floor??
    ## prepare stuff
    bincenters=[]; rawhisto=[]
    
    # initialize histo
    for i in range(nbin):
        rawhisto.append(0.0)
        bincenters.append(xmin + float(i) * dx + dx/2.0)
    
    # fill rawhisto
    for i,d in enumerate(rawdatapair):
        # check if within boundaries
        if(d<xmin or d>=xmax): continue
        index = int(math.floor((d-xmin)/dx))
        rawhisto[index] += ws_raw_pair[i]
        
    # normalize 
    normrawh = sum(rawhisto)
        
    for i in range(len(rawhisto)):
       
        rawhisto[i] = rawhisto[i] / normrawh

    return rawhisto,nbin, bincenters
    
def get_FRETR_GFP_names(pair):

    internal_fret_residues={'700':'700','765':'761','795':'791'}
 
    gfp_tag=["CFP","YFP"]

    new_pair=[]

    for i in range(len(pair)):
        prot=pair[i].split('-')[0].rstrip('p')
        terminus=pair[i].split('-')[1]

        if terminus =="C":
            fretdomain=prot+"-"+gfp_tag[i]

        elif terminus =="N":
            fretdomain=gfp_tag[i]+"-"+prot

        elif terminus in internal_fret_residues:
            fretdomain=prot+"_"+gfp_tag[i]+"i@"+internal_fret_residues[terminus]

        new_pair.append(fretdomain)

    if new_pair[0]=="Spc42-CFP" and new_pair[1]=="YFP-Spc42":
        new_pair[0]="YFP-Spc42-CFP"
        new_pair[1]="YFP-Spc42-CFP"

    return tuple(new_pair)

fig = plt.figure()

print "Plotting"

for i, pair in enumerate(data["name"]):

    ax = fig.add_subplot(7,6,i+1)
    
    # the histogram of the data
    histo_models, nbins_models, bincenters_models = get_histo_models(fmod[pair], ww_models, 0.75, 3.25) 
    # histogram, normalized already in the function.
    ax.step(bincenters_models,histo_models,color="black",linewidth=1.0)

    histo_raw, nbins_raw, bincenters_raw = get_histo_raw(rawdata[pair], ww_raw[pair], 0.75, 3.25) 
    # red line corresponding to experiment 
    ax.step(bincenters_raw,histo_raw,color="red", linewidth=1.0)
    
    ymax = max(max(histo_models),max(histo_raw))
       
    if(i>=36):   ax.set_xlabel(r'FRET$_R$', fontsize=12,fontname='Arial')
    if(i%6==0): ax.set_ylabel(r'P',fontsize=12,fontname='Arial')
    ax.set_xlim(0.75, 3.35)
    #ax.set_ylim(0.0,1.0)
    ax.set_ylim(0.0,ymax)

    title_pair=get_FRETR_GFP_names(pair)
    if title_pair[0]==title_pair[1]: #YFP-SPC42-CFP
       ax.set_title(str(i+1)+". "+title_pair[0], position=(0.5, 1.00),fontsize=6,fontname='Arial')

    elif "@" in title_pair[0] or "@" in title_pair[1]:
        ax.set_title(str(i+1)+". "+title_pair[0]+" "+title_pair[1], position=(0.5, 1.00), fontsize=5,fontname='Arial')
    else:
       ax.set_title(str(i+1)+". "+title_pair[0]+" "+title_pair[1], position=(0.5, 1.00), fontsize=6,fontname='Arial')
    
    ax.tick_params(labelsize=5)

    plt.locator_params(axis='y',nbins=6)

    # hide the spines between ax00 and ax01
    if(i<36): ax.tick_params(labelbottom='off')
    #if(i%6!=0): ax.tick_params(labelleft='off')
 
fig.tight_layout(pad=0.1,w_pad=0.05, h_pad=0.05)
#fig.set_size_inches(6.8,5.4)
plt.savefig("fret_fit_"+OUTFILE_SUFFIX_+".pdf",dpi=300)
