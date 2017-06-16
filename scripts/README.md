## Note: 
Please also refer to  
(1) the README.md in the [spb module] (https://github.com/salilab/spb) for the description of each executable along with its inputs and outputs.  
(2) the README.md in the config_files directory that shows what the options are for each executable.

Here we describe how to run the modeling protocol with the executables from the SPB C++ module. The scripts from each directory are described in the order they are used.  
Each directory also contains a version of the scripts for testing (starting with `test_`) in addition to the production scripts (that were used in the actual modeling).

## 1. Sample
In this step, SPB models are sampled using Well-Tempered Ensemble Replica Exchange Gibbs Sampling Monte Carlo. 

Create a directory for sampling (called `SAMPLING`, for example), make it the current working directory.  
   - **Inputs:**  The files that need to be in the current directory include:
        - inputs for sampling (`inputs/shared_inputs`; see README in `inputs` directory)  
        - sampling config file (see `config_files` directory)  

    - **Running:**  The script for sampling can be run as in  
    `sh sample_local.sh` for running on a local machine; and using the job script `job_sample.sh` for running on a cluster.  
    Both these use MPI and are 8 core jobs. Note that the number of cores should be 8 since it is using well-tempered ensemble (WTE) Replica Exchange and the number of cores has been optimized based on the exchange acceptance rate. Also note that this can take about 5-6 days to run (on a machine like pico), and about 10 days on the Salilab cluster.

    - **Outputs:**  The script should produce `traj*.rmf` which are RMF files that store model coordinates and `trajisd*.rmf` that store ISD coordinates such as FRET parameters, cell size and so on. Also `log*` files show the time step, temperature, FRET forward model values and parameters, FRET and yeast two-hybrid scores, Bias values, cell size, CP layer size, and other parameters at each step.

    - **Test version:** For testing the code, the same inputs can be used with the test config file for sampling (see `config_files` directory), which executes a shorter sampling run (5000 steps instead of 120000 steps) and which can be run on a single core like below (`$IMPDIR` is the location of the IMP build directory).  
    `sh test_sample.sh $IMPDIR`

## 2. Preparation for analysis
After sampling is complete, to prepare models for analysis, one needs to first extract the frames at temperature 1K from the sampling.   
The below script can be run in `SAMPLING`, and produces a file called `Index_Replica0`.   
`sh get_Index_Replica.sh` 

Also, one needs to obtain the correct bias file for reweighting in the next step of analysis. This is performed by the following code that provides an output file BIAS. BIAS is the bias file at the end of the simulation corresponding to the replica at T=1.  
`sh get_bias_file.sh`

## 3. Analysis
In this step, the sampled models at temperature 1K are rescored with the EM2D restraint (which is too expensive to use in sampling) as well as FRET and other restraints. 

In the parent directory of `SAMPLING`, create a new directory to store the ensemble of models at T=1 (call it `RMF` for example).   
Create another directory for analysis in the same directory as `RMF` and `SAMPLE` (called `ANALYSIS`), make it the current working directory.  
Create a `DATA` sub-directory in `ANALYSIS` that will contain the input data for analyzing each frame (at temperature 1K) from sampling.   

