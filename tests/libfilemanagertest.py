# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:12:26 2013

@author: shanef
"""

import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from libfilemanager import EncodeData


class libfilemanagertest(unittest.TestCase):
    def test_EncodeDataPrint(self):
        showname = "test show"
        inputname = "test input"
        outputname = "test output"
        data = EncodeData(showname, inputname, outputname)
        result = str(data)
        expected = "Show: {0}\nInput: {1}\nOutput: " \
               "{2}\n".format(showname, inputname, outputname)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(libfilemanagertest)
    unittest.TextTestRunner(verbosity=2).run(suite)