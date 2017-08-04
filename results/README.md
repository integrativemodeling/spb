The folders in this directory correspond to models obtained in initial and final modeling runs (refer to the paper for what these mean). 
They are organized by clusters, numbered according to the paper.

Each cluster contains:

- **Top scoring model** : `top_scoring_model.rmf`, top scoring model representing the cluster, can be visualized using UCSF Chimera.   
  To color the model according to the paper use `scripts/chimera/color_model_chimera_commands.txt`.  
  Load it as a Chimera commands file after loading the model in Chimera.
      
- **Per-bead densities** : `*.dx`, localization probability density maps for the cluster. 

  To visualize these in Chimera, run the followin in the directory containing
the models and densities:
    `scripts/chimera/create_chimera_command_file_densities.sh HM.dat`
      This will create a file called `chimera_density_command_lines.txt`.  
      Now open Chimera with the top scoring model RMF and then load the `chimera_density_command_lines.txt` as a Chimera commands file. This should show all the densities.
      
- **Fret fit plots** :  plots showing fit of models in the cluster to FRET data.
  - **summary plot** : `fret_summary.pdf` shows how the average model FRET fits with the average experimental FRET.  
  - **distribution plot**: `fret_distribution.pdf` visualizes the distribution of model and experimental FRET values for each FRET pair.
  
#### Full trajectories and clustered models
The actual trajectories and clustered models are also available as follows:
- **initial models (2x Spc29)**: The run name is **c42xtal_dist29**.
  - [Sampling](https://zenodo.org/record/838791/files/sampling_c42xtal_dist29.tar.xz)
  - [Analysis and everything else](https://zenodo.org/record/838791/files/clustering_c42xtal_dist29.tar.xz)

- **final models (1x Spc29)**: The run names are **one29_c42xtal_dist29** and **second_one29_c42xtal_dist29** (run 1 and run 2, the two independent runs). The results shown in the paper are for the set of models obtained by merging these two runs. The files are:
  - Sampling [one29\_c42xtal\_dist29](https://zenodo.org/record/838791/files/sampling_one29_c42xtal_dist29.tar.xz) and [second\_one29\_c42xtal\_dist29](https://zenodo.org/record/838791/files/sampling_second_one29_c42xtal_dist29.tar.xz)
  - Analysis [one29\_c42xtal\_dist29](https://zenodo.org/record/838791/files/clustering_one29_c42xtal_dist29.tar.xz) and [second\_one29\_c42xtal\_dist29](https://zenodo.org/record/838791/files/clustering_second_one29_c42xtal_dist29.tar.xz)
  - Analysis for the merged set of models [sample\_conv](https://zenodo.org/record/838791/files/clustering_sample_conv.tar.xz)
