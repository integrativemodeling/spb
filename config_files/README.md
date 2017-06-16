The parameters appearing in the config files can be grouped as 
  - General parameters that are needed for any SPB executable, and 
  - Parameters that are specific to different stages of modeling.

Details of parameters are documented in the config files.   
Note that each SPB executable has a config file in its own directory.  
Config files for production code (used in the actual modeling) have been separated from those for test runs.

## General parameters (applicable for all SPB executables)
These are found in all config files under `SPB Proteins`, `Cell information`, `Restraints`, `Parameters for FRET_R`, and `Use new FRET_R data on Spc110p coiled-coil`. 

## Sampling-specific parameters 
These are also found in all config files under `Parameters Gibbs sampling` and `WTE`.  
Note that the test config files differ in the number of MC steps (only 5000 steps compared to 120000 steps in the production runs).

## Analysis-specific parameters
These are only found at the end of config files in `analysis`, under `Parameters specific to analysis` and describe EM2D parameters and model/parameter file names for analysis.

## Clustering-specific parameters
These are only found at the end of config files in `cluster`, under `Parameters specific to clustering` and describe model file names and clustering parameters such as cutoff, number of models to cluster and so on. 

## Density map-specific parameters
These are only found at the end of config files in `cluster`, under `Parameters specific to density` 


