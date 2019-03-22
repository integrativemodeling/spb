
#!/usr/bin/env python

"""Collect data on the yeast Spindle Pole Body core and output an mmCIF file suitable for
   deposition at PDB-Dev, https://pdb-dev.wwpdb.org/. This uses the python-ihm
   library, available at https://github.com/ihmwg/python-ihm.
"""

import ihm.dumper
import ihm.representation
import ihm.model
import ihm.protocol
import ihm.dataset
import ihm.analysis
import rmf_file
import os

system = ihm.System(title='Yeast spindle pole body core')

system.citations.append(ihm.Citation(
          pmid='28814505',
          title="The molecular architecture of the yeast spindle pole "
                "body core determined by Bayesian integrative modeling.",
            journal="Mol Biol Cell", volume=28, page_range=(3298,3314),
          year=2017,
          authors=['Viswanath S', 'Bonomi M', 'Kim SJ',
                   'Klenchin VA', 'Taylor KC', 'Yabut KC', 'Umbreit NT', 'van Epps HA',
                   'Meehl J', 'Jones MH', 'Russel D',
                   'Velazquez-Muriel JA', 'Winey M', 'Rayment I', 'Davis TN', 'Sali A', 'Muller EG'],
          doi='10.1091/mbc.E17-06-0397'))

#########################################
######### SOFTWARE USED ##################
#########################################
# We used Modeller to build homology models for Spc110-Cmd1 complex
system.software.append(ihm.Software(
          name='Modeller', classification='protein homology modeling',
          description='Protein homology modeling',
          version='9v8',
          location='https://salilab.org/modeller/'))

# We used CCCP server to build coiled-coil models for several subunits
cccp = ihm.Software(
          name='CCCP', classification='coiled-coil modeling',
          description='Coiled-coil model construction by Crick parametrization',
          location='https://arteni.cs.dartmouth.edu/cccp/index.gen.php')
system.software.append(cccp)

# We used various tools from IMP (e.g. FoXS)
imp = ihm.Software(
          name="Integrative Modeling Platform (IMP)",
          version="2.3",
          classification="integrative model building",
          description="integrative model building",
          location='https://integrativemodeling.org')
system.software.append(imp)

# Software to process the SAXS data.
system.software.append(ihm.Software(
          name="ATSAS",
          version="2.8.3",
          classification="SAXS data processing",
          description="calculate ab-initio shape, rg, dmax and pair distribution function",
          location='https://www.embl-hamburg.de/biosaxs/software.html'))

system.software.append(ihm.Software(
          name="SAXSMoW",
          classification="SAXS data processing",
          description="calculate molecular weight from SAXS",
          location='https://saxs.ifsc.usp.br/'))

#########################################
######### DATASETS ######################
#########################################
# 1. PDB data
spc110_cmd1_pdb = ihm.dataset.Dataset(ihm.location.PDBLocation('4DS7'))

cnm67_cterm_pdb = ihm.dataset.Dataset(ihm.location.PDBLocation('3OA7'))

gfp_pdb = ihm.dataset.Dataset(ihm.location.PDBLocation('1EMA'))

#TODO How do we link these PDBs to the representation? I am lost here. 

# 2. FRET dataset
fret_data = ihm.dataset.FRETDataset(ihm.location.InputFileLocation('fret_data.doc',repo=ihm.location.Repository(
          doi="10.5281/zenodo.1219204",
          url="https://zenodo.org/record/1209565/files/fret.zip"), details="Pairwise in-vivo FRET data points on SPB core proteins"))

# 3. SAXS dataset
# SAXS profile of Spc110-Cmd1 monomer was used for validating the comparative model
# SAXS profile of Spc110-Cmd1 dimer was used for forming pairwise distance restraints on the dimer structure 
# SAXS profile of Spc29 was used for restraining its length 
saxs_profiles = ihm.dataset.SASDataset(ihm.location.InputFileLocation('Figure_2_SAXS_Spc110_Cmd1_Spc29.gif',repo=ihm.location.Repository(
          doi="10.5281/zenodo.1219204",
          url="https://zenodo.org/record/1209565/files/saxs.zip"), details="SAXS profiles of Spc110-Cmd1 and Spc29 used for validating    the comparative model and forming restraints for modeling"))

# Molecular weights of Spc110-Cmd1 and Spc29 from SAXS were used for validation.
saxs_molecular_weights = ihm.dataset.Dataset(ihm.location.InputFileLocation('Table_Molecular_Weights.xlsx',repo=ihm.location.Repository(
          doi="10.5281/zenodo.1219204",
          url="https://zenodo.org/record/1209565/files/saxs.zip"), details="Molecular weight estimation from SAXS for Spc110-Cmd1 and Spc29"))

# 4. Y2H dataset
# Y2H modeling data
y2h_modeling_data_list = []
for biogrid_id in [142827,142847,142849]:
   y2h_modeling_data_list.append(ihm.dataset.YeastTwoHybridDataset(ihm.location.BioGRIDLocation(biogrid_id)))
y2h_modeling_data = ihm.dataset.DatasetGroup(y2h_modeling_data_list)

# Y2H validation data
y2h_validation_data_list = []
for biogrid_id in [142825,142826]:
   y2h_validation_data_list.append(ihm.dataset.YeastTwoHybridDataset(ihm.location.BioGRIDLocation(biogrid_id)))
y2h_validation_data = ihm.dataset.DatasetGroup(y2h_validation_data_list)

# 5. EM map
em2d_dataset = ihm.dataset.Dataset(ihm.location.InputFileLocation('bullitt_1999_em2d_map.tiff',repo=ihm.location.Repository(
          doi="10.5281/zenodo.1219204",
          url="https://zenodo.org/record/1209565/files/bullitt_1999_em2d_map.tiff"), details="Tomogram of overexpressed Spc42 from Bullitt et al 1999"))

# 6. Biochemical site data
# this data is from biochemical annalysis of the Cnm67 PDB structure, so don't need to list a separate dataset here.

# 7. Layer localization data
# this is based on immuno-EM. 
#TODO How to cite it? 

# 8. Genetic screens dataset
genetic_screens_dataset = ihm.dataset.Dataset(ihm.location.InputFileLocation('Results\ of\ screens.png',repo=ihm.location.Repository(
          doi="10.5281/zenodo.1219204",
          url="https://zenodo.org/record/1209565/files/genetic_screens.zip"), details="Genetic screening to validate position of Spc110 in the CP")
                                            
                                              
# 9. EM labeling data
em_labeling_dataset = ihm.dataset.Dataset(ihm.location.InputFileLocation('em_labeling.png',repo=ihm.location.Repository(
          doi="10.5281/zenodo.1219204",
          url="https://zenodo.org/record/1209565/files/em_labeling.png"), details="EM labeling results for setting the stoichiometry of Spc29 in the models")
                                         
#########################################
######### Representation  ###############
#########################################

(entities_by_name, representation,
        density_map) = rmf_file.make_representation(system, cccp)

assembly = ihm.Assembly(system.asym_units[:], name='Modeled assembly')

#########################################
######### RESTRAINTS  ###################
#########################################
# Refer Table S6, S1 in the paper.





#########################################
######### MODELING PROTOCOL  ############
#########################################

protocol = ihm.protocol.Protocol(name='Modeling')

protocol.steps.append(ihm.protocol.Step(
                 assembly=assembly, dataset_group=None,
                 method='Monte Carlo',
                 name='Monte Carlo Gibbs sampling by parallel tempering '
                      'in the well-tempered ensemble',
                 num_models_begin=1, num_models_end=48000,
                 software=imp))

# todo: fill in correct numbers of models
analysis = ihm.analysis.Analysis()
analysis.steps.append(ihm.analysis.ClusterStep(
                feature='RMSD', num_models_begin=48000, num_models_end=48000,
                assembly=assembly, dataset_group=None))
protocol.analyses.append(analysis)

#########################################
######### VALIDATION, FIT TO DATA? ######
#########################################





#########################################
######### FINAL OUTPUTS #################
#########################################

# Single state
state = ihm.model.State()
system.state_groups.append(ihm.model.StateGroup([state]))

# Clusters
for with_spc29, num in ('without', '2.1'), ('with', '2.2'), ('with', '2.3'):
    subdir = os.path.join('..', 'final_models_1x_Spc29',
                          'cluster_%s_Spc29' % with_spc29, 'cluster%s' % num)
    fname = os.path.join(subdir, 'top_scoring_model.rmf')
    m = rmf_file.Model(assembly=assembly, protocol=protocol,
                       representation=representation, file_name=fname,
                       asym_units=system.asym_units)
    mg = ihm.model.ModelGroup([m], name='All models in cluster %s' % num)
    state.append(mg)
    # todo: fill in correct number of ensemble models
    e = ihm.model.Ensemble(model_group=mg, num_models=999,
                           name='All models in cluster %s' % num)
    # Add localization densities
    for density_name, rnglist in density_map.items():
        fname = os.path.join(subdir, density_name + '.dx')
        if os.path.exists(fname):
            loc = ihm.location.OutputFileLocation(fname)
            for rng in rnglist:
                d = ihm.model.LocalizationDensity(file=loc, asym_unit=rng)
                e.densities.append(d)
    system.ensembles.append(e)


# Write out in mmCIF format
with open('spb.cif', 'w') as fh:
    ihm.dumper.write(fh, [system])
