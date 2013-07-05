# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 14:40:38 2013

@author: shane
"""
import ProcessRecordings
import unittest
from minimock import mock
import os.path


class ProcessRecordingsTest(unittest.TestCase):
    def test_fixnumber(self):
        result = ProcessRecordings.FixEpisodeSeasonNumber(1)
        self.assertEqual("01", result)
    
    def test_fixnumber2(self):
        result = ProcessRecordings.FixEpisodeSeasonNumber(9)
        self.assertEqual("09", result)

    def test_fixnumber3(self):
        result = ProcessRecordings.FixEpisodeSeasonNumber(11)
        self.assertEqual("11", result)
    
    def test_episodeName(self):
        subtitle = 'Mike the Knight and the Test Case'
        title = 'Mike the Knight'
        result = ProcessRecordings.GetEpisodeName(subtitle, title)
        self.assertEqual('Test Case', result)
    
    def test_episodeName2(self):
        subtitle = 'Test Case 2'
        title = 'Mike the Knight'
        result = ProcessRecordings.GetEpisodeName(subtitle, title)
        self.assertEqual('Test Case 2', result)
        
    def test_GetDirectoryThomas(self):
        title = 'Thomas and Friends'
        season = 'Season 01'
        result = ProcessRecordings.GetDirectory(title, season)
        self.assertEqual("/srv/storage2/files/VideoProcessing/Thomas/Input/Season 01", result)

    def test_GetDirectoryThomas2(self):
        title = 'Thomas the Tank Engine & Friends'
        season = 'Season 01'
        result = ProcessRecordings.GetDirectory(title, season)
        self.assertEqual("/srv/storage2/files/VideoProcessing/Thomas/Input/Season 01", result)
    
    def test_GetDirectoryChuggington(self):
        title = 'Chuggington'
        season = 'Season 02'
        result = ProcessRecordings.GetDirectory(title, season)
        self.assertEqual("/srv/storage2/files/VideoProcessing/Chuggington/Input/Season 02", result)
    
    def test_DetermineTargetFilename(self):
        directory = '/srv/storage2/test/Input'
        filename = 'S01E02 - test episode - SD TV_.mpg'
        inputFilename = '123456.mpg'
        
        mock('os.path.exists', returns=True)
        result = ProcessRecordings.DetermineTargetFilename(directory, filename, inputFilename)
        self.assertEqual('/srv/storage2/test/Input/123456/S01E02 - test episode - SD TV_.mpg', result)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ProcessRecordingsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)