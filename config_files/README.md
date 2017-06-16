### Note 
Each parameter in the config file is documented directly in the config file.  
Note that each SPB executable has a config file in its own directory.  
Config files for production code (used in the actual modeling) have been separated from those used for test runs.

The parameters appearing in the config files can be grouped as 
  - General parameters that are needed for any SPB executable, and 
  - Parameters that are specific to different stages of modeling.

## General parameters (applicable for all SPB executables)
These are found in all config files under `SPB Proteins`, `Cell information`, `Restraints`, `Parameters for FRET_R`, and `Use new FRET_R data on Spc110p coiled-coil`. 

## Sampling-specific parameters 
These are also found in all config files under `Parameters Gibbs sampling` and `WTE`.  
Note that the test config files differ in the number of MC steps (only 5000 steps compared to 120000 steps in the production runs).

## Analysis-specific parameters
These are only found at the end of config files in `analysis`, under `Parameters specific to analysis` and describe EM2D parameters and model/parameter file names for analysis.

## Clustering-specific parameters
These are only found at the end of config files in `cluster`, under `Parameters specific to clustering` and describe model file names and clustering parameters such as cutoff, number of models to cluster and so on. 
Note that the test config files differ in the number of models to cluster (only 1000 compared to 24000 in the production runs).

## Density map-specific parameters
These are only found at the end of config files in `density_perbead`, under `Parameters specific to density` and include parameters such as voxel size, reference model for calculating density and so on.


