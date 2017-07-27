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

    def test_sampling(self):
        """Test sampling step"""
        os.chdir(TOPDIR)
        shutil.rmtree('test-sampling', ignore_errors=True)
        os.mkdir('test-sampling')
        os.chdir('test-sampling')
        # Get all needed input files
        shutil.copy('../config_files/test/sample/config.ini', '.')
        for f in glob.glob('../inputs/shared_inputs/*'):
            shutil.copy(f, '.')
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

if __name__ == '__main__':
    unittest.main()
