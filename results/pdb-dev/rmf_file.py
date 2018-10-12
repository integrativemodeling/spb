import IMP
import RMF
import IMP.rmf
import IMP.atom
import IMP.pmi.topology
import os
import ihm

def make_representation(system):
    """Using one of the output RMFs as a guide, create the IHM representation"""
    fname = os.path.join('..', 'final_models_1x_Spc29', 'cluster_without_Spc29',
                         'cluster2.1/top_scoring_model.rmf')
    seqs = IMP.pmi.topology.Sequences(os.path.join('..', '..', 'inputs',
                                                'shared_inputs', 'seqs.fasta'))
    entities_by_name = {}

    m = IMP.Model()
    rh = RMF.open_rmf_file_read_only(fname)
    hs = IMP.rmf.create_hierarchies(rh, m)
    for h in hs:
        name = h.get_name()
        entity_name = 'GFP' if name.endswith('GFP') else name
        if entity_name not in entities_by_name:
            e = ihm.Entity(seqs[entity_name], description=entity_name)
            system.entities.append(e)
            entities_by_name[entity_name] = e
        asym = ihm.AsymUnit(entities_by_name[entity_name], details=name)
        system.asym_units.append(asym)
    return entities_by_name
