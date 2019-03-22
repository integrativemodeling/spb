import IMP
import RMF
import IMP.rmf
import IMP.atom
import IMP.pmi.topology
import os
import ihm
import ihm.startmodel

def _get_starting_coiled_coil_datasets():
    """Get the starting coiled-coil datasets.
       Some parts of the system were identified as coiled-coil and so the
       starting structures for the simulation were taken from ideal coiled-coil
       structures generated with CCCP. These come in two lengths - 120 and
       78 residues. Return a mapping from length to the files used
       (per chain)."""
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
    """Using one of the output RMFs as a guide, create the IHM representation
       (i.e. the subunits in the system and how residues are represented
       as beads)."""
    fname = os.path.join('..', 'final_models_1x_Spc29', 'cluster_without_Spc29',
                         'cluster2.1/top_scoring_model.rmf')
    seqs = IMP.pmi.topology.Sequences(os.path.join('..', '..', 'inputs',
                                                'shared_inputs', 'seqs.fasta'))
    ccdatasets = _get_starting_coiled_coil_datasets()

    # Mapping from RMF names of subunits to ihm.Entity objects
    entities_by_name = {}
    # Map from localization density filename to list of asym ranges
    density_map = {}
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
        _add_density_map(h, asym, density_map)

    system.orphan_representations.append(rep)
    return entities_by_name, rep, density_map

def _add_density_map(hier, asym, density_map):
    """Assign domains to localization density maps"""
    # see also get_map() in IMP::spb's spb_density_perbead.cpp
    name_map = {"Spc110":"Spc110p", "Cmd1":"Cmd1p", "Cnm67":"Cnm67p",
                "Spc42_CC":"Spc42_CC", "Spc42p_c0":"Spc42p_c0",
                "Spc42p_c1":"Spc42p_c1", "Spc42p_c2":"Spc42p_c2",
                "Spc42p_n0":"Spc42p_n0", "Spc29p_n0":"Spc29p_n0",
                "Spc29p_n1":"Spc29p_n1", "Spc29p_n2":"Spc29p_n2",
                "Spc29p_c0":"Spc29p_c0", "Spc29p_c1":"Spc29p_c1",
                "Spc29p_c2":"Spc29p_c2"}
    def get_density(bead):
        name = bead.get_name()
        for domainfrag, density_name in name_map.items():
            if domainfrag in name:
                return density_name

    for c in hier.get_children():
        den = get_density(c)
        if den:
            rng = IMP.atom.Domain(c).get_index_range()
            if den not in density_map:
                density_map[den] = [asym(rng[0], rng[1]-1)]
            else:
                # Combine this bead with previous if they are contiguous
                prev = density_map[den][-1]
                if prev.asym == asym \
                   and prev.seq_id_range[1] == rng[0] - 1:
                    density_map[den][-1] = asym(prev.seq_id_range[0], rng[1]-1)
                else:
                    density_map[den].append(asym(rng[0], rng[1]-1))

def _add_asym_representation(hier, asym, rep, ccdatasets, cccp):
    """Add representation for the given chain (hier, asym) to rep"""
    segments = []
    numbeads = []
    coiled_coils = []
    rigids = []
    # Go through all RMF particles for this chain and collect into segments
    # of beads with the same representation
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
        # Tell ihm that this segment was represented by beads
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


class Model(ihm.model.Model):
    """Pass an RMF model through to IHM"""
    def __init__(self, file_name, asym_units, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.file_name = file_name
        self.asym_units = asym_units

    def get_spheres(self):
        # Traverse the RMF file, and yield ihm.model.Sphere objects for
        # each bead
        m = IMP.Model()
        rh = RMF.open_rmf_file_read_only(self.file_name)
        hs = IMP.rmf.create_hierarchies(rh, m)
        for h, asym in zip(hs, self.asym_units):
            for bead in h.get_children():
                assert IMP.atom.Domain.get_is_setup(bead)
                assert IMP.core.XYZR.get_is_setup(bead)
                rng = IMP.atom.Domain(bead).get_index_range()
                xyzr = IMP.core.XYZR(bead)
                coord = xyzr.get_coordinates()
                # rng[1]-1 because IHM ranges are inclusive but Domain
                # ranges aren't
                # todo: fix range for GFP
                yield ihm.model.Sphere(asym_unit=asym,
                                       seq_id_range=(rng[0], rng[1]-1),
                                       x=coord[0], y=coord[1], z=coord[2],
                                       radius=xyzr.get_radius())
