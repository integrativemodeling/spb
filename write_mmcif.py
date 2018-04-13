
#!/usr/bin/env python

import ihm.dumper
import ihm.representation
import ihm.model
import ihm.protocol
import ihm.analysis
import pdb
import saxs
import em2d
import compmodel

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
system.software.append(ihm.Software(
          name='CCCP', classification='coiled-coil modeling',
          description='Coiled-coil model construction by Crick parametrization',
          location='https://arteni.cs.dartmouth.edu/cccp/index.gen.php'))
# We used various tools from IMP (e.g. FoXS)
system.software.append(ihm.Software(
          name="Integrative Modeling Platform (IMP)",
          version="2.3",
          classification="integrative model building",
          description="integrative model building",
          location='https://integrativemodeling.org'))

# Software to process the SAXS data.
system.software.append(ihm.Software(
          name="ATSAS",
          version="2.8.3"
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
######### SYSTEM  #######################
#########################################

How do you represent this? 

Do you add cell size, and layer size as 
part of the representation?






#########################################
######### RESTRAINTS  ###################
#########################################

#########################################
######### MODELING PROTOCOL  ############
#########################################







#########################################
######### VALIDATION, FIT TO DATA? ######
#########################################





#########################################
######### FINAL OUTPUTS #################
#########################################

# Localization densities are in the Ensemble class.
# Why is there no support to add densities? 
# In IM those are as important as, if not more important than the models. 



