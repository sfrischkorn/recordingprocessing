# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 23:13:15 2013

@author: shanef
"""

import unittest
from minimock import Mock
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import libtvdatasource


class tvdatasourceTest(unittest.TestCase):
    def test_GetOutputFilenameNoIllegals(self):
        result = self._dooutputfilenametest("S01", "E02", "test name", "")
        self.assertEqual(result, "S01E02 - test name - SD TV_.mpg")

    def test_GetOutputFilenameOneIllegals(self):
        result = self._dooutputfilenametest("S01", "E02", "test name?", "?")
        self.assertEqual(result, "S01E02 - test name - SD TV_.mpg")

    def test_GetOutputFilenameTwoIllegals(self):
        result = self._dooutputfilenametest("S01", "E02", "tes>t name?", ["?", ">"])
        self.assertEqual(result, "S01E02 - test name - SD TV_.mpg")

    def _dooutputfilenametest(self, season, episode, name, illegals):
        settings = Mock('libsettings.Settings')
        settings.illegalcharacters.mock_returns = illegals
        tvdatasource = libtvdatasource.TVData(settings)
        return tvdatasource.getoutputfilename(season, episode, name)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(tvdatasourceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)