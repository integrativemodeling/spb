## Note: 
Please also refer to  
 1. the documentation of the [IMP.spb module](https://integrativemodeling.org/nightly/doc/ref/namespaceIMP_1_1spb.html) for the description of each executable along with its inputs and outputs.  
 2. the config files in the `config_files` directory that shows what the options are for each executable.

Here we describe how to run the modeling protocol with the executables from the SPB C++ module. The scripts from each directory are described in the order they are used.  
Each directory also contains a version of the scripts for testing (starting with `test_`) in addition to the production scripts (that were used in the actual modeling).

In each step below, `$SPB` denotes the top-level directory of this repository
(this README is `$SPB/scripts/README.md`).

## 1. Sample
In this step, SPB models are sampled using Well-Tempered Ensemble Replica Exchange Gibbs Sampling Monte Carlo. 

Create a directory for sampling called `SAMPLING`, and make it the current
working directory.
   - **Inputs:**  The files that need to be copied into the `SAMPLING`
     directory include:
        - inputs for sampling (`inputs/shared_inputs`; see README in `inputs` directory)  
        - sampling config file (see `config_files/production/sample/`
          directory)  
          
   - **Running:**  The sampling can be done in the `SAMPLING` directory by
      simply running "`mpirun -np 8 spb`". This is an MPI job using one core
      for each replica. The number of replicas has been optimized as 8
      based on the exchange acceptance rate. This will typically take 5-10
      days to run on a modern Linux box or cluster. The actual SGE script used
      for running on a cluster can be found as
      `scripts/sample/job_sample.sh`.
      
   - **Outputs:**  The script should produce `traj*.rmf` which are RMF files that store model coordinates and `trajisd*.rmf` that store ISD coordinates such as FRET parameters, cell size and so on. Also `log*` files show the time step, temperature, FRET forward model values and parameters, FRET and yeast two-hybrid scores, Bias values, cell size, CP layer size, and other parameters at each step.
   
   - **Test version:** For testing the code, the same inputs can be used with
      a test config file for sampling (see `config_files/test/sample/`
      directory), which executes a shorter sampling run (5000 steps instead
      of 120000 steps).

## 2. Preparation for analysis
After sampling is complete, to prepare models for analysis, one needs to first extract the frames at temperature 1K from the sampling.   
The below script can be run in the `SAMPLING` directory, and produces a file
called `Index_Replica0`.
`$SPB/scripts/sampling/get_Index_Replica.sh`

Also, one needs to obtain the correct bias file for reweighting in the next step of analysis. This is performed by the following code that provides an output file BIAS. BIAS is the bias file at the end of the simulation corresponding to the replica at T=1.  
`$SPB/scripts/sampling/get_bias_file.sh`

## 3. Analysis
In this step, the sampled models at temperature 1K are rescored with the EM2D restraint (which is too expensive to use in sampling) as well as FRET and other restraints. 

In the parent directory of `SAMPLING`, create a new directory to store the ensemble of models at T=1, called `RMF`.
Create another directory for analysis in the same directory as `RMF` and `SAMPLE` (called `ANALYSIS`), make it the current working directory.  
Create a `DATA` sub-directory in `ANALYSIS` that will contain the input data for analyzing each frame (at temperature 1K) from sampling.

   - **Inputs:** The following files need to be in the `DATA` directory:  
      - The `BIAS` file from the sampling directory
      - Inputs for analysis (`inputs/analysis`) along with shared inputs (`inputs/shared_inputs`)
      - Config file for analysis (see `config_files`) 
      
   - **Running:** The sample SGE script provided (`scripts/analysis/job_analysis.sh`) extracts and rescores multiple frames in a (trivially) parallel manner. Each frame at temperature 1K is extracted from the trajectories output from sampling, stored in the directory `RMF`, and rescored with the EM2D restraint.    
   
   - **Outputs:** Frames (models) at temperature 1 K are extracted from the sampling trajectories and placed in a separate folder with one model per RMF. For each frame that is rescored, 2 files are output: `fret.dat` (contains FRET score and FRET forward model values) and `log.dat` (contains model weight, model score, the EM2D score, and other parameters such as unit cell size for the model). 
   
   - **Test version:** The frames created in the test sampling run can be analysed using the test script as below. Do not forget to use the test config script (see `config_files` directory) while running the test script.
      `$SPB/scripts/analysis/test_analysis.sh`
     
## 4. Cluster 
In this step, rescored models are clustered, considering the model weight obtained in the previous (analysis) step.  

In the parent directory of `ANALYSIS`, create another directory called `CLUSTER`, and make it the current working directory.

   - **Inputs:** The inputs that need to be in this directory for clustering include:  
        - Inputs for clustering (`inputs/cluster`): a label file `label.dat` that specifies which beads to use for clustering  
        - Shared inputs (`inputs/shared_inputs`)  
        - Config file for clustering (see `config_files`)

   - **Running:** The sample SGE script provided (`scripts/cluster/job_cluster.sh`) runs clustering (takes ~8 hrs on one core).  

   - **Outputs:** The outputs are 3 files: `cluster_center.dat` (File containing list of clusters, one per line. Each line has cluster population, model corresponding to cluster center, cluster diameter and mean distance between models in the cluster.),  `cluster_distance.dat` (Pairwise distances between cluster centers) and `cluster_traj_score_weight.dat` (File with one line per model: each line containing model number, cluster it belongs to, model score, model weight and unit cell size in the model).   
   
   - **Test version:** The frames created in the test sampling run can be analysed using the test script as below, run in the `CLUSTER` directory. Do not forget to use the test config script (see `config_files` directory) while running the test script.
`$SPB/scripts/cluster/test_cluster.sh`

**Note:** Running the following script in the `CLUSTER` directory
gives the model number for the top scoring model of cluster `$CLUSTER_NUMBER`, and stores it in the file `top_scoring_model_cluster_$CLUSTER_NUMBER.rmf`.
`$SPB/scripts/cluster/get_top_scoring_model.sh $CLUSTER_NUMBER`

## 5. Compute density maps
In this step, localization probability density maps are created for desired clusters. Note that some proteins such as Cnm67, Cmd1 and Spc110 are represented by a single density map each, while others like Spc42 and Spc29 have multiple domains that are represented in different density maps.

In the parent directory of `CLUSTER`, create another directory called `MAKE_DENSITY_PERBEAD`, and make it the current working directory.

   - **Inputs:** The inputs that need to be in this directory include:    
        - Shared inputs (`inputs/shared_inputs`)  
        - Config file for density maps (see `config_files`)
        
   - **Running:** The sample SGE script provided
     (`scripts/density_perbead/job_density_perbead.sh`) runs density
     calculation for cluster 0, in less than an hour on 64 cores.
     (This step will run faster on more cores - unlike the sampling step the
     number of cores doesn't have to match the number of replicas used.)
     
   - **Outputs:** The outputs are files `*.dx` corresponding to the densities of different proteins and domains. Also generated is a file `HM.dat`, that provides the value of the densities at half the maximum (for visualization in Chimera).
    
   - **Test version:** The frames clustered in the test clustering run can be visualized by running the test script from the `MAKE_DENSITY_PERBEAD` directory as below Do not forget to use the test config (see `config_files` directory) while running the test script.
    `$SPB/scripts/density_perbead/test_density_perbead.sh`

To visualize the densities, they can be loaded in Chimera as follows. First,
run the following script from within the `MAKE_DENSITY_PERBEAD` directory:
    `$SPB/scripts/chimera/create_chimera_command_file_densities.sh HM.dat`

This will create a file called `chimera_density_command_lines.txt`. Now open Chimera with the top scoring model RMF for the cluster and then load the `chimera_density_command_lines.txt` as a Chimera commands file. This should show all the densities.

## 6. Compute FRET fit
In this step, the average FRETR value and the distribution of FRETR values from the models is compared to the averages and distributions of FRETR from experiment.

In the parent directory of `CLUSTER`, create another directory called `FRET_FIT` (say), and make it the current working directory.

   - **Inputs:**
       - the `cluster_traj_score_weight.dat` file produced by the
         clustering step, above.
       - `fret_exp.dat`: the file containing FRET averages and standard deviations from experiment
       - `rawdata_all_date.csv` : file containing the raw FRET values from experiment. 
       The last 2 files are in `inputs/fretfit`. 
       
   - **Running:**  The scripts can be run as below, in the `FRET_FIT` directory
     (`CLUSTER_NUMBER` is the number of the cluster we are interested in;
      `SUFFIX` names the output file).
    `$SPB/scripts/fretfit/plot_FRETR_summary.py CLUSTER_NUMBER ../CLUSTER/cluster_traj_score_weight.dat ../ANALYSIS fret_exp.dat SUFFIX`
    `$SPB/scripts/fretfit/plot_FRETR_distribution.py CLUSTER_NUMBER ../CLUSTER/cluster_traj_score_weight.dat ../ANALYSIS fret_exp.dat rawdata_all_date.csv SUFFIX`

   - **Outputs:** The summary and distribution scripts produce
`fretsummary_SUFFIX_clusterCLUSTER_NUMBER.pdf` and
`fret_fit_SUFFIX_cluster_CLUSTER_NUMBER.pdf` respectively.
