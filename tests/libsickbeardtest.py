# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:12:38 2013

@author: shanef
"""

import unittest
from minimock import Mock
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import libsickbeard
import urllib


class SickbeardTest(unittest.TestCase):
    def test_findepisodeCloseSubtitle(self):
        settings = Mock('libsettings.Settings')
        settings.sickbeardaddress.mock_returns = "test"
        settings.sickbeardport.mock_returns = "test"
        settings.sickbeardapikey.mock_returns = "test"

        urllib.urlopen = dummy_urlopen

        sickbeard = libsickbeard.Sickbeard(settings)

        result = sickbeard.findepisode("78949", "Splish, Splash, Splosh")

        self.assertEqual("13", result[0])
        self.assertEqual("15", result[1])
        self.assertEqual("Splish, Splash, Splosh!", result[2])


def dummy_urlopen(arg):
    class TmpClass:
        def read(arg):
            jsonresult = '{ "data": {"13": { "15": { "airdate": "2010-02-12", ' \
                         '"name": "Splish, Splash, Splosh!", "quality": "N/A", ' \
                         '"status": "Wanted" } } }, "message": "", ' \
                         '"result": "success" }'

            return jsonresult

    return TmpClass()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SickbeardTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
