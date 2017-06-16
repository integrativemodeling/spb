The folders in this directory correspond to models obtained in initial and final modeling runs (refer to the paper for what these mean). 
They are organized by clusters, numbered according to the paper.

Each cluster contains:

    - `top_scoring_model.rmf` : Top scoring model representing the cluster, can be visualized using UCSF Chimera. 
To color the model according to the paper use `scripts/chimera/color_model_chimera_commands.txt`. Load it as a Chimera commands file after loading the model on Chimera.

    - `Per bead densities`: \*.dx files. To visualize these in chimera, enter the following line in the terminal: `sh create_chimera_command_file_densities.sh $pdir names_colors HM.dat` where $pdir is your working directory where the models and densities are stored (full global path: can be obtained by the command `pwd` on linux), names_colors and HM.dat should be in the same directory as the densities. 
This will create a file called `chimera_density_command_lines.txt`. Now open Chimera with the top scoring model RMF and then load the `chimera_density_command_lines.txt` as a Chimera commands file. This should show all the densities.

    - Fret fit plots: 
        * summary plot: shows how the average model FRET fits with the average experimental FRET.
        * distribution plot: visualizes the distribution of model and experimental FRET values for each FRET pair. 

The location of the actual trajectories and clustered models on disk is as follows:
    - `initial models (2x Spc29)`: The run name is *c42xtal_dist29*. The output of sampling is at /salilab/park1/shruthi/spb/sampling/c42xtal\_dist29 and analysis (and everything else) is at /salilab/park1/shruthi/spb/clustering/c42xtal\_dist29.

- `final models (1x Spc29)`: The run names are *one29_c42xtal_dist29* and *second_one29_c42xtal_dist29* (run 1 and run 2, the two independent runs). The results shown in the paper are for the set of models obtained by merging these two runs. The directories are: sampling (`/salilab/park1/shruthi/spb/sampling/one29_c42xtal_dist29` and `/salilab/park1/shruthi/spb/sampling/second_one29_c42xtal_dist29`), analysis (`/salilab/park1/shruthi/spb/clustering/one29_c42xtal_dist29` and `/salilab/park1/shruthi/spb/clustering/second_one29_c42xtal_dist29`, and finally for the merged set of models `/salilab/park1/shruthi/spb/clustering/sample_conv`). 








