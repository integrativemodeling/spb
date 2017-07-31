#!/usr/bin/env python

import unittest
import os
import sys
import subprocess
import glob
import shutil
import re
import RMF

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

class Tests(unittest.TestCase):

    def get_file_length(self, fname):
        """Get the number of lines in the file"""
        with open(fname) as fh:
            return len(fh.readlines())

    def _check_rmf_file(self, r, frames, toplevel_children):
        """Check an RMF file for expected size"""
        self.assertEqual(r.get_number_of_frames(), frames)
        rn = r.get_root_node()
        self.assertEqual(len(rn.get_children()), toplevel_children)

    def _check_sample_rmf_traj(self, fname):
        """Check the RMF trajectory"""
        r = RMF.open_rmf_file_read_only(fname)
        # Test config asked for 5000 steps, saving every 5
        self._check_rmf_file(r, frames=1000, toplevel_children=609)
        # Test topology
        rn = r.get_root_node()
        topol = rn.get_children()
        self.assertEqual(topol[0].get_name(), 'Spc42p')
        self.assertEqual(topol[10].get_name(), 'Spc42p-N-GFP')
        self.assertEqual(topol[600].get_name(), 'Spc110p-C-GFP')

    def _check_sample_rmf_isd_traj(self, fname):
        """Check the RMF ISD trajectory"""
        r = RMF.open_rmf_file_read_only(fname)
        # Test config asked for 5000 steps, saving every 5
        self._check_rmf_file(r, frames=1000, toplevel_children=15)

    def _get_inputs(self, subdir, dirname):
        """Copy all input files from inputs/`subdir` to `dirname`"""
        for f in glob.glob('%s/inputs/%s/*' % (TOPDIR, subdir)):
            shutil.copy(f, dirname)

    def _get_shared_inputs(self, dirname):
        """Copy all shared input files to `dirname`"""
        self._get_inputs('shared_inputs', dirname)

    def test_modeling(self):
        """Test complete modeling run"""
        self.test_dir = os.path.join(TOPDIR, 'test-output')

        shutil.rmtree(self.test_dir, ignore_errors=True)
        os.mkdir(self.test_dir)
        self.run_sampling_step()
        self.run_analysis_step()
        self.run_clustering_step()

    def run_analysis_step(self):
        """Run the analysis part of the modeling"""
        os.chdir(self.test_dir)
        os.mkdir('ANALYSIS')
        os.mkdir('ANALYSIS/DATA')
        os.mkdir('RMF')
        # Get all needed input files
        shutil.copy('SAMPLING/BIAS', 'ANALYSIS/DATA')
        shutil.copy('%s/config_files/test/analysis/config.ini' % TOPDIR,
                    'ANALYSIS/DATA')
        self._get_shared_inputs('ANALYSIS/DATA')
        self._get_inputs('analysis', 'ANALYSIS/DATA')
        # Run analysis script
        subprocess.check_call(["%s/scripts/analysis/test_analysis.sh" % TOPDIR])
        # Make sure expected files were produced
        for i in range(1000):
            for fname in ('fret.dat', 'log.dat'):
                self.assertTrue(os.path.exists(os.path.join(
                                             'ANALYSIS','frame_%d' % i, fname)))
            for (prefix, toplevel_children) in (('frame', 609),
                                                ('frameisd', 15)):
                fname = os.path.join('RMF', '%s_%d.rmf' % (prefix, i))
                r = RMF.open_rmf_file_read_only(fname)
                self._check_rmf_file(r, frames=1,
                                     toplevel_children=toplevel_children)

    def run_sampling_step(self):
        """Run the sampling part of the modeling"""
        sample_dir = os.path.join(self.test_dir, 'SAMPLING')
        os.mkdir(sample_dir)
        os.chdir(sample_dir)
        # Get all needed input files
        shutil.copy('%s/config_files/test/sample/config.ini' % TOPDIR, '.')
        self._get_shared_inputs('.')
        # Run on two processors
        p = subprocess.check_call(["mpirun", "-n", "2", "spb"])
        # Make sure expected files were produced
        for fname in ('log0', 'log1', 'traj0.rmf', 'trajisd0.rmf',
                      'traj1.rmf', 'trajisd1.rmf', 'BIAS0', 'BIAS1'):
            self.assertTrue(os.path.exists(fname))
        self._check_sample_rmf_traj('traj0.rmf')
        self._check_sample_rmf_traj('traj1.rmf')

        self._check_sample_rmf_isd_traj('trajisd0.rmf')
        self._check_sample_rmf_isd_traj('trajisd1.rmf')

        # Prepare files for analysis
        subprocess.check_call(["%s/scripts/sample/get_Index_Replica.sh"
                               % TOPDIR])
        self.assertEqual(self.get_file_length("Index_Replica0"), 1000)

        subprocess.check_call(["%s/scripts/sample/get_bias_file.sh" % TOPDIR])
        self.assertEqual(self.get_file_length("BIAS"), 8162)

    def run_clustering_step(self):
        """Run the clustering part of the modeling"""
        os.chdir(self.test_dir)
        os.mkdir('CLUSTER')
        os.chdir('CLUSTER')
        # Get all needed input files
        shutil.copy('%s/config_files/test/cluster/config.ini' % TOPDIR, '.')
        self._get_shared_inputs('.')
        self._get_inputs('cluster', '.')
        # Run clustering script
        subprocess.check_call(["%s/scripts/cluster/test_cluster.sh" % TOPDIR])
        # Check outputs
        num_clusters = self.get_file_length("cluster_center.dat") - 1
        self.assertEqual(self.get_file_length("cluster_distance.dat"),
                         num_clusters * (num_clusters-1) / 2 + 1)
        self.assertEqual(self.get_file_length("cluster_traj_score_weight.dat"),
                         1001)
        for i in range(num_clusters):
            # Check the top-scoring-model script
            subprocess.check_call(["%s/scripts/cluster/get_top_scoring_model.sh"
                                   % TOPDIR, str(i)])
            self.assertTrue(os.path.exists('top_scoring_model_cluster_%d.rmf'
                                           % i))

if __name__ == '__main__':
    unittest.main()
