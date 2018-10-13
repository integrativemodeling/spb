import IMP
import RMF
import IMP.rmf
import IMP.atom
import IMP.pmi.topology
import os
import ihm
import ihm.startmodel

def _get_starting_coiled_coil_datasets():
    """Get the starting coiled-coil datasets"""
    ccpath = "../../inputs/shared_inputs"
    datasets = {120:[], 78:[]}

    for length in (120, 78):
        for chain in ('A', 'B'):
            p = os.path.join(ccpath, "CC_%d_%s.pdb" % (length, chain))
            l = ihm.location.InputFileLocation(p,
                     details="Idealized coiled-coil structure generated using "
                             "CCCP with default Crick parameters")
            d = ihm.dataset.PDBDataset(l)
            d.spb_chain = chain
            datasets[length].append(d)
    return datasets

def make_representation(system, cccp):
    """Using one of the output RMFs as a guide, create the IHM representation"""
    fname = os.path.join('..', 'final_models_1x_Spc29', 'cluster_without_Spc29',
                         'cluster2.1/top_scoring_model.rmf')
    seqs = IMP.pmi.topology.Sequences(os.path.join('..', '..', 'inputs',
                                                'shared_inputs', 'seqs.fasta'))
    ccdatasets = _get_starting_coiled_coil_datasets()

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
        _add_asym_representation(h, asym, rep, ccdatasets, cccp)

    system.orphan_representations.append(rep)
    return entities_by_name, rep

def _add_asym_representation(hier, asym, rep, ccdatasets, cccp):
    """Add representation for asym to rep"""
    segments = []
    numbeads = []
    coiled_coils = []
    rigids = []
    for c in hier.get_children():
        coiled_coil = '_CC' in c.get_name()
        rigid = IMP.core.RigidMember.get_is_setup(c)
        assert IMP.atom.Domain.get_is_setup(c)
        rng = IMP.atom.Domain(c).get_index_range()
        # Join neighboring beads into one segment, unless one bead is
        # a coiled call and the other isn't
        # rng[1]-1 because IHM ranges are inclusive but Domain ranges aren't
        if segments and segments[-1][1] == rng[0] - 1 \
           and coiled_coil == coiled_coils[-1] and rigid == rigids[-1]:
            segments[-1][1] = rng[1] - 1
            numbeads[-1] += 1
        else:
            segments.append([rng[0], rng[1] - 1])
            numbeads.append(1)
            coiled_coils.append(coiled_coil)
            rigids.append(rigid)
    for seg, nbead, coiled_coil, rigid in zip(segments, numbeads,
                                              coiled_coils, rigids):
        # RMF says 3 50-residue beads represent GFP, starting at residue 0,
        # but GFP really has 238 residues, so adjust accordingly
        if 'GFP' in hier.get_name() and seg == [0,149]:
            seg = [1,238]
        smodel = None
        if coiled_coil:
            smodel = _get_coiled_coil_starting_model(asym, seg, ccdatasets,
                                                     cccp)
        rep.append(ihm.representation.FeatureSegment(asym(*seg), rigid=rigid,
                                                     primitive='sphere',
                                                     count=nbead,
                                                     starting_model=smodel))

def _get_coiled_coil_starting_model(asym, seg, ccdatasets, cccp):
    """Get starting model for a coiled-coil region"""
    length = seg[1] - seg[0] + 1
    # Get coiled-coil starting model of correct length, and ensure we
    # get the other one next time
    ds = ccdatasets[length][0]
    ccdatasets[length] = list(reversed(ccdatasets[length]))
    return ihm.startmodel.StartingModel(asym(*seg), dataset=ds,
                    asym_id=ds.spb_chain, offset=seg[0]-1, software=cccp)
