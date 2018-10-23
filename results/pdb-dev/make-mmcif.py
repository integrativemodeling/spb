
#!/usr/bin/env python

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
# PDB 


# FRET dataset
fret_repo = ihm.location.Repository(doi='10.  /zenodo.   ',
        url='https://zenodo.org/record/  /files/archive.zip')
fret_location = ihm.location.InputFileLocation("??", repo=fret_repo)
system.locations.append(fret_location)

fret_data = ihm.dataset.Dataset(fret_location)

# SAXS dataset
saxs_repo = ihm.location.Repository(doi='10.  /zenodo.   ',
        url='https://zenodo.org/record/  /files/archive.zip')
saxs_mol_wt_location = ihm.location.InputFileLocation("", repo=saxs_repo)
saxs_profiles_location = ihm.location.InputFileLocation("",repo=saxs_repo)
system.locations.append(saxs_mol_wt_location)
system.locations.append(saxs_profiles_location)

saxs_mow_data = ihm.dataset.Dataset(saxs_mol_wt_location)
saxs_shape_rg_data = ihm.dataset.Dataset(saxs_mol_wt_location)

# Y2H dataset




# EM map



# Biochemical site info


# Layer localization info


# Genetic screens dataset
genetic_screens_repo = ihm.location.Repository(doi='10.  /zenodo.   ',
        url='https://zenodo.org/record/  /files/archive.zip')
genetic_screens_location = ihm.location.InputFileLocation("??", repo=genetic_screens_repo)
system.locations.append(genetic_screens_location)

genetic_screens_data = ihm.dataset.Dataset(genetic_screens_location)

#########################################
######### Representation  ###############
#########################################

entities_by_name, representation = rmf_file.make_representation(system, cccp)

assembly = ihm.Assembly(system.asym_units[:], name='Modeled assembly')

#########################################
######### RESTRAINTS  ###################
#########################################

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
    fname = os.path.join('..', 'final_models_1x_Spc29',
                         'cluster_%s_Spc29' % with_spc29, 'cluster%s' % num,
                         'top_scoring_model.rmf')
    m = rmf_file.Model(assembly=assembly, protocol=protocol,
                       representation=representation, file_name=fname,
                       asym_units=system.asym_units)
    mg = ihm.model.ModelGroup([m], name='All models in cluster %s' % num)
    state.append(mg)
    # todo: fill in correct number of ensemble models
    e = ihm.model.Ensemble(model_group=mg, num_models=999,
                           name='All models in cluster %s' % num)
    # todo: add localization densities to e.densities
    system.ensembles.append(e)


# Write out in mmCIF format
with open('spb.cif', 'w') as fh:
    ihm.dumper.write(fh, [system])
