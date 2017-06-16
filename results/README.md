The folders in this directory correspond to models obtained in initial and final modeling runs (refer to the paper for what these mean). 
They are organized by clusters, numbered according to the paper.

Each cluster contains:

- **Top scoring model** : `top_scoring_model.rmf`, top scoring model representing the cluster, can be visualized using UCSF Chimera.   
  To color the model according to the paper use `scripts/chimera/color_model_chimera_commands.txt`.  
  Load it as a Chimera commands file after loading the model on Chimera.
      
- **Per-bead densities** : `*.dx`, localization probability density maps for the cluster. 

  To visualize these in Chimera, enter the following line in the terminal:   
  `sh create_chimera_command_file_densities.sh $pdir names_colors HM.dat` where `$pdir` is your working directory where the models and densities are stored (full global path: can be obtained by the command `pwd` on linux). `names_colors` and `HM.dat` should be in the same directory as the densities.  
      This will create a file called `chimera_density_command_lines.txt`.  
      
      Now open Chimera with the top scoring model RMF and then load the `chimera_density_command_lines.txt` as a Chimera commands file. This should show all the densities.
      
- **Fret fit plots** :  plots showing fit of models in the cluster to FRET data.
  - **summary plot** : `fret_summary.pdf` shows how the average model FRET fits with the average experimental FRET.  
  - **distribution plot**: `fret_distribution.pdf` visualizes the distribution of model and experimental FRET values for each FRET pair.
