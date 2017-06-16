This folder contains the inputs needed for different stages of modeling.
Some input files are shared across multiple stages of modeling.

## 1) shared_inputs:
These inputs are used to run the executables for sampling (executable: `spb`), rescoring with EM restraint (executable: `spb_analysis`), clustering (executable: `spb_cluster`), and density calculation (executable: `spb_density` and `spb_density_perbead`).

    - 3OA7_A.pdb, 3OA7_B.pdb: PDB structure of Cnm67-C terminus. 
    - 4DS7_*_swapped.pdb: homology models of Spc110-Cmd1 dimer without the domain swap.
    - CC_78_A.pdb, CC_78_B.pdb: coiled-coil domain of Spc42.
    - CC_120_A.pdb,CC_120_B.pdb: coiled-coil domain of Spc110.
    - fret_2014.dat: reshot FRET data between SPB protein termini.
    - fret_new_exp.dat : internal FRET between Spc110-coiled coil and other SPB proteins.

## 2) analysis:
The extra input for this step is the EM map (`SPB_2d_padded.tiff`) since we rescore with EM2D restraint in this step.

## 3) cluster:
The extra input for this step is `label.dat` the file containing the bead labels on which clustering is performed.

## 4) fretfit: 
We use the raw FRET data (`rawdata_all_date.csv`) to get the experimental FRET distributions and compare them to the model FRET distributions.
`fret_exp.dat` contains the experimental averages and standard deviations (data is identical to the FRET files used in sampling, with a minor change in format). 
