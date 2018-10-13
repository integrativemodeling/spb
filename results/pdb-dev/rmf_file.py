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
    rep = ihm.representation.Representation()

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
        _add_asym_representation(h, asym, rep)

    system.orphan_representations.append(rep)
    return entities_by_name, rep

def _add_asym_representation(hier, asym, rep):
    """Add representation for asym to rep"""
    segments = []
    numbeads = []
    last_coiled_coil = None
    for c in hier.get_children():
        coiled_coil = '_CC' in c.get_name()
        assert IMP.atom.Domain.get_is_setup(c)
        rng = IMP.atom.Domain(c).get_index_range()
        # Join neighboring beads into one segment, unless one bead is
        # a coiled call and the other isn't
        # rng[1]-1 because IHM ranges are inclusive but Domain ranges aren't
        if segments and segments[-1][1] == rng[0] - 1 \
           and coiled_coil == last_coiled_coil:
            segments[-1][1] = rng[1] - 1
            numbeads[-1] += 1
        else:
            segments.append([rng[0], rng[1] - 1])
            numbeads.append(1)
        last_coiled_coil = coiled_coil
    for seg, nbead in zip(segments, numbeads):
        # RMF says 3 50-residue beads represent GFP, starting at residue 0,
        # but GFP really has 238 residues, so adjust accordingly
        if 'GFP' in hier.get_name() and seg == [0,149]:
            seg = [1,238]
        # todo: add starting model where appropriate
        rep.append(ihm.representation.FeatureSegment(asym(*seg), rigid=False,
                                                     primitive='sphere',
                                                     count=nbead))
