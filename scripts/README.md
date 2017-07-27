## Note: 
Please also refer to  
 1. the documentation of the [IMP.spb module](https://integrativemodeling.org/nightly/doc/ref/namespaceIMP_1_1spb.html) for the description of each executable along with its inputs and outputs.  
 2. the config files in the `config_files` directory that shows what the options are for each executable.

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

   - **Inputs:** The following things need to be in the `DATA` directory:  
      - The `BIAS` file from the sampling directory
      - Inputs for analysis (`inputs/analysis`) along with shared inputs (`inputs/shared_inputs`)
      - Config file for analysis (see `config_files`)
        
    - **Running:** The sample SGE script provided (`job_analysis.sh`) extracts and rescores multiple frames in a (trivially) parallel manner. Each frame at temperature 1K is extracted from the trajectories output from sampling, stored in the directory `RMF`, and rescored with the EM2D restraint. 
    
    - **Outputs:** Frames (models) at temperature 1 K are extracted from the sampling trajectories and placed in a separate folder with one model per RMF. For each frame that is rescored, 2 files are output: `fret.dat` (contains FRET score and FRET forward model values) and `log.dat` (contains model weight, model score, the EM2D score, and other parameters such as unit cell size for the model). 
    
    - **Test version:** The frames created in the test sampling run can be analysed using the test script as below (`$IMPDIR` is the location of the IMP build directory). Do not forget to use the test config script (see `config_files` directory) while running the test script.  
      `sh test_analysis.sh $IMPDIR`
     
## 4. Cluster 
In this step, rescored models are clustered, considering the model weight obtained in the previous (analysis) step.  

In the parent directory of `ANALYSIS`, create another directory called `CLUSTER` (say), make it the current working directory.

   - **Inputs:** The inputs that need to be in this directory for clustering include:  
        - Inputs for clustering (`inputs/cluster`): a label file `label.dat` that specifies which beads to use for clustering  
        - Shared inputs (`inputs/shared_inputs`)  
        - Config file for clustering (see `config_files`)

   - **Running:** The sample SGE script provided (`job_cluster.sh`) runs clustering (takes ~8 hrs on one core).  

   - **Outputs:** The outputs are 3 files: `cluster_center.dat` (File containing list of clusters, one per line. Each line has cluster population, model corresponding to cluster center, cluster diameter and mean distance between models in the cluster.),  `cluster_distance.dat` (Pairwise distances between cluster centers) and `cluster_traj_score_weight.dat` (File with one line per model: each line containing model number, cluster it belongs to, model score, model weight and unit cell size in the model).   

   - **Test version:** The frames created in the test sampling run can be analysed using the test script as below (`$IMPDIR` is the location of the IMP build directory). Do not forget to use the test config script (see `config_files` directory) while running the test script.  
`sh test_cluster.sh $IMPDIR`  

**Note:** Running the following script gives the model number for the top scoring model of cluster `$CLUSTER_NUMBER`, and stores it in the file `top_scoring_model_cluster_$CLUSTER_NUMBER.rmf`.  
`sh get_top_scoring_model.sh $CLUSTER_NUMBER` 

## 5. Compute density maps
In this step, localization probability density maps are created for desired clusters. Note that some proteins such as Cnm67, Cmd1 and Spc110 are represented by a single density map each, while others like Spc42 and Spc29 have multiple domains that are represented in different density maps.

In the parent directory of `CLUSTER`, create another directory called `MAKE_DENSITY_PERBEAD` (say), make it the current working directory.

   - **Inputs:** The inputs that need to be in this directory include:    
        - Shared inputs (`inputs/shared_inputs`)  
        - Config file for density maps (see `config_files`)

   - **Running:** The sample SGE script provided (`job_density_perbead.sh`) runs density calculation for cluster 0, in less than an hour on 64 cores.

    - **Outputs:** The outputs are files `*.dx` corresponding to the densities of different proteins and domains. Also provided is a file `HM.dat`, that provides the value of the densities at half the maximum (for visualization in Chimera). 

    - **Test version:** The frames clustered in the test clustering run can be visualized using the test script as below (`$IMPDIR` is the location of the IMP build directory). Do not forget to use the test config script (see `config_files` directory) while running the test script.  
`sh test_density_perbead.sh $IMPDIR` 

To visualize the densities, they can be loaded in Chimera as follows. Enter the following line in the terminal:   
`sh create_chimera_command_file_densities.sh $pdir names_colors HM.dat`.  

The files `create_chimera_command_file_densities.sh`,`names_colors` can be found in the `scripts/chimera` directory, and `$pdir` is your working directory where the models and densities are stored (it is the full global path: can be obtained by the command `pwd` on linux). HM.dat should be in the same directory as the densities.  

This will create a file called `chimera_density_command_lines.txt`. Now open Chimera with the top scoring model RMF for the cluster and then load the `chimera_density_command_lines.txt` as a Chimera commands file. This should show all the densities.

## 6. Compute FRET fit
In this step, the average FRETR value and the distribution of FRETR values from the models is compared to the averages and distributions of FRETR from experiment.

In the parent dictory of `CLUSTER`, create another directory called `FRET_FIT` (say), make it the current working directory.

   - **Inputs:**
       - `id.weight.cluster`: a file containing 2 columns: model/frame ID in the first, model weight in the second, for models in the cluster we are interested in.
       - `fret_exp.dat`: the file containing FRET averages and standard deviations from experiment
       - `rawdata_all_date.csv` : file containing the raw FRET values from experiment. 
       The last 2 files are in `inputs/fretfit`. 
       
   - **Running:**  The scripts can be run as below (`CLUSTER_NUMBER` is the number of the cluster we are interested in; `SUFFIX` is the name of the output file).  
`python plot_FRETR_summary.py CLUSTER_NUMBER id.weight.cluster ../ANALYSIS fret_exp.dat SUFFIX`  
`python plot_FRETR_distribution.py CLUSTER_NUMBER id.weight.cluster ../ANALYSIS fret_exp.dat rawdata_all_date.csv SUFFIX`

   - **Outputs:** The summary and distribution scripts produce `fret_summary.pdf` and `fret_distribution.pdf` respectively.
