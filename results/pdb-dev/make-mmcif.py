
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
# PDB data
spc110_cmd1_pdb = ihm.dataset.Dataset(ihm.location.PDBLocation('4DS7'))

cnm67_cterm_pdb = ihm.dataset.Dataset(ihm.location.PDBLocation('3OA7'))

gfp_pdb = ihm.dataset.Dataset(ihm.location.PDBLocation('1EMA'))

#TODO How do we link these PDBs to the representation? I am lost here. 

# FRET dataset
fret_data = ihm.dataset.Dataset(ihm.location.DatabaseLocation(,repo=ihm.location.Repository(
          doi="10.5281/zenodo.1209565", root="../../%s" % subdir,
          url="https://zenodo.org/record/1209565/files/%s.zip" % zipname,
          top_directory=os.path.basename(subdir))

# SAXS dataset, incl. molecular weights

# Y2H dataset




# EM map



# Biochemical site info


# Layer localization info


# Genetic screens dataset

# EM labeling info



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
