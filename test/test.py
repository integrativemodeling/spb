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

    def assert_file_length(self, fname, num_lines):
        """Make sure that the given file has the right number of lines"""
        with open(fname) as fh:
            lines = fh.readlines()
        self.assertEqual(len(lines), num_lines)

    def _check_sample_rmf_traj(self, fname):
        """Check the RMF trajectory"""
        r = RMF.open_rmf_file_read_only(fname)
        # Test config asked for 5000 steps, saving every 5
        self.assertEqual(r.get_number_of_frames(), 1000)
        # Test topology
        rn = r.get_root_node()
        topol = rn.get_children()
        self.assertEqual(len(topol), 609)
        self.assertEqual(topol[0].get_name(), 'Spc42p')
        self.assertEqual(topol[10].get_name(), 'Spc42p-N-GFP')
        self.assertEqual(topol[600].get_name(), 'Spc110p-C-GFP')

    def _check_sample_rmf_isd_traj(self, fname):
        """Check the RMF ISD trajectory"""
        r = RMF.open_rmf_file_read_only(fname)
        # Test config asked for 5000 steps, saving every 5
        self.assertEqual(r.get_number_of_frames(), 1000)
        # Test topology
        rn = r.get_root_node()
        topol = rn.get_children()
        self.assertEqual(len(topol), 15)

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
        self.assert_file_length("Index_Replica0", 1000)

        subprocess.check_call(["%s/scripts/sample/get_bias_file.sh" % TOPDIR])
        self.assert_file_length("BIAS", 8162)


if __name__ == '__main__':
    unittest.main()
