
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

system = ihm.System()

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
# Gazillion software to process the SAXS data. Should I list those? 




# Localization densities are in the Ensemble class.
# Why is there no support to add densities? 
# In IM those are as important as, if not more important than the models. 



