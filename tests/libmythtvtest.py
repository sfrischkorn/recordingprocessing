# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:12:53 2013

@author: shanef
"""

import unittest
from minimock import Mock
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
import libmythtv

class MythTVTest(unittest.TestCase):
    def test_FixEpisodeNameNoPrefix(self):
        settings = Mock('libsettings.Settings')
        settings.GetShowMythTVEpisodePrefix.mock_returns = ""
        mythtv = libmythtv.MythTV(settings)
        result = mythtv.FixMythTVEpisodeName("Show", "episode")
        self.assertEqual(result, "episode")

    def test_FixEpisodeNameNonMatchingPrefix(self):
        settings = Mock('libsettings.Settings')
        settings.GetShowMythTVEpisodePrefix.mock_returns = [ "BloohBlah" ]
        mythtv = libmythtv.MythTV(settings)
        result = mythtv.FixMythTVEpisodeName("Show", "episode")
        self.assertEqual(result, "episode")

    def test_FixEpisodeNameMatchingPrefix(self):
        settings = Mock('libsettings.Settings')
        settings.GetShowMythTVEpisodePrefix.mock_returns = [ "Match " ]
        mythtv = libmythtv.MythTV(settings)
        result = mythtv.FixMythTVEpisodeName("Show", "Match episode")
        self.assertEqual(result, "episode")

    def test_FixEpisodeNameMatchingFirstPrefix(self):
        settings = Mock('libsettings.Settings')
        settings.GetShowMythTVEpisodePrefix.mock_returns = [ "Match and ", "Match the " ]
        mythtv = libmythtv.MythTV(settings)
        result = mythtv.FixMythTVEpisodeName("Show", "Match and episode")
        self.assertEqual(result, "episode")
        
    def test_FixEpisodeNameMatchingSecondPrefix(self):
        settings = Mock('libsettings.Settings')
        settings.GetShowMythTVEpisodePrefix.mock_returns = [ "Match and ", "Match the " ]
        mythtv = libmythtv.MythTV(settings)
        result = mythtv.FixMythTVEpisodeName("Show", "Match the episode")
        self.assertEqual(result, "episode")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MythTVTest)
    unittest.TextTestRunner(verbosity=2).run(suite)