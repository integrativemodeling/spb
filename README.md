This repository pertains to the molecular architecture of the yeast spindle pole body (SPB), the structural and functional equivalent of the metazoan centrosome. Data from in vivo FRET and yeast two-hybrid, along with SAXS, X-ray crystallography, and electron microscopy were integrated by a Bayesian structure modeling approach.

The repository contains input data, scripts for modeling and results including bead models and localization probability density maps. It uses [IMP](https://integrativemodeling.org)

## Prerequisites for running the code
Note that the SPB code is almost fully written in C++ and uses native IMP, unlike most other recent integrative modeling projects that use PMI. 
The SPB code is in [Github](https://github.com/salilab/spb) and must be compiled as a module with a recent version of IMP. [MPI](https://integrativemodeling.org/2.7.0/doc/ref/namespaceIMP_1_1mpi.html) must be used to compile the IMP code so that replica exchange can be used. 


## Folder structure:
1) _inputs_ : contains all the input data used for modeling such as PDB files, FRET experimental values, and so on.
2) _config_: contains the config files for each step of modeling: these have the parameters used for each step.
3) _results_ : contains the results of initial and final modeling runs, showing the models and localization densities of various clusters, along with the fit to FRET data. 
4) _scripts_ : configuration files, bash scripts and sample scripts to run jobs on the cluster are provided, that call the SPB C++ code. 

## Information
_Author(s)_: Shruthi Viswanath, Massimiliano Bonomi

_Date_: June 6th, 2017

_License_: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License.

_Last known good IMP version_: [![build info](https://integrativemodeling.org/systems/?sysstat=23&branch=master)](https://integrativemodeling.org/systems/) [![build info](https://integrativemodeling.org/systems/?sysstat=23&branch=develop)](https://integrativemodeling.org/systems/)

_Testable_: Yes.

_Parallelizeable_: Yes

_Publications_:
 - S. Viswanath, M. Bonomi, S.J. Kim, N.T. Umbreit, K. Taylor, D. Klenchin, K. Yabut, H.A.Van Epps, J. Meehl, M.H. Jones, D. Russel, J.A. Velazquez-Muriel, M. Winey, I. Rayment, T.N. Davis, A. Sali, and E.G. Muller, The molecular architecture of the yeast spindle pole body core determined by Bayesian integrative modeling, submitted.
