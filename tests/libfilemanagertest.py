# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:12:26 2013

@author: shanef
"""

import unittest
import os
import sys
import minimock
from minimock import mock
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

    def test_EncodeDataCheckProblemsFileExists(self):
        showname = "test show"
        inputname = "test input"
        outputname = "test_output.mkv"
        data = EncodeData(showname, inputname, outputname)
        mock("os.path.exists", returns=True)

        result = data.checkproblems()

        self.assertIn("FILE_EXISTS", result)

    def test_EncodeDataCheckProblemsFile_Exists(self):
        showname = "test show"
        inputname = "test input"
        outputname = "test_output_.mkv"
        data = EncodeData(showname, inputname, outputname)
        mock("os.path.exists", returns_iter=[False, True])
        result = data.checkproblems()
        self.assertIn("FILE_EXISTS", result)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(libfilemanagertest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    minimock.restore()
