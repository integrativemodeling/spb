This document describes the parameters appearing in the config files.

## General parameters (applicable for all SPB executables)
  - **SPB proteins**  
    - `resolution`: the number of residues per bead to represent the protein when there is an atomic model. 
    - `add_*`: Boolean that specifies whether to include a protein in the simulation/analysis.
    - `load_*`: RMF file to load the coordinates of a protein from.
 
  - **GFP-related**
    - `use_GFP_structure`: whether to use the crystal structure of GFP.
    - `keep_GFP_layer`: whether to restrain GFPs in the corresponding layers (CP/IL2)
    - `GFP_exc_volume`: whether to consider GFPs while calculating excluded volume  
    - `fix_GFP`: whether to fix the position of GFPs during refinement (not used)
    - `restraint_GFP`: whether to restrain the position of GFPs during refinement (not used)

  - **Cell-size and layer thickness**
     - `` :
     - `` :
     

  - **FRET-specific**

  - **Other restraints**

## Sampling-specific parameters 
  - **b**


## Analysis-specific parameters

## Clustering-specific parameters

## Density map-specific parameters



