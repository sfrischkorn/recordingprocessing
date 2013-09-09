# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:12:26 2013

@author: shanef
"""

import unittest
import os
import sys
import minimock
from minimock import mock, Mock
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from libfilemanager import EncodeData, FileManager


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
        minimock.restore()

    def test_EncodeDataCheckProblemsFile_Exists(self):
        showname = "test show"
        inputname = "test input"
        outputname = "test_output_.mkv"
        data = EncodeData(showname, inputname, outputname)
        mock("os.path.exists", returns_iter=[False, True])
        result = data.checkproblems()
        self.assertIn("FILE_EXISTS", result)
        minimock.restore()

    def test_checkfileexistscaseinsensitive(self):
        settings = Mock('libsettings.Settings')
        filemanager = FileManager(settings)

        mock("os.listdir", returns=["filename.test"])

        result = filemanager.checkfileexists("/path/to/fiLename.test", False)

        self.assertTrue(result)
        minimock.restore()

    def test_checkduplicateavi(self):
        settings = Mock('libsettings.Settings')
        filemanager = FileManager(settings)

        os.walk = dummywalk

        result = filemanager.checkduplicates("/path/to/S03E14 - Test - SD TV.mkv")

        self.assertTrue(result)
        minimock.restore()

    def test_checkduplicatethomas(self):
        settings = Mock('libsettings.Settings')
        filemanager = FileManager(settings)

        os.walk = thomaswalk

        result = filemanager.checkduplicates("/path/to/S12E05 - Henry Gets It Wrong - SD TV.mkv")

        self.assertTrue(result)
        minimock.restore()

    def test_checkduplicatenomatch(self):
        settings = Mock('libsettings.Settings')
        filemanager = FileManager(settings)

        os.walk = dummywalk

        result = filemanager.checkduplicates("/path/to/S03E13 - Test - SD TV.mkv")

        self.assertFalse(result)
        minimock.restore()

    def test_checkduplicatesameextension(self):
        settings = Mock('libsettings.Settings')
        filemanager = FileManager(settings)

        os.walk = dummywalk

        result = filemanager.checkduplicates("/path/to/S03E14 - Test - SD TV.avi")

        self.assertFalse(result)
        minimock.restore()



def dummywalk(arg):
    return [("/path/to/", [], ["S03E14 - Test - SD TV.avi"])]

def thomaswalk(arg):
    return [(("/path/to/", [], ["S12E05 - Henry Gets It Wrong - Unknown.AVI"]))]

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(libfilemanagertest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    minimock.restore()
