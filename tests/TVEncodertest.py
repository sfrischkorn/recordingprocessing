# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 20:37:47 2013

@author: shanef
"""

import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import TVEncoder


class TVEncoderTest(unittest.TestCase):
    def test_processarguments_encodereadonly(self):
        args = []
        args.append(('-e', ''))
        args.append(('-l', ''))
        result = TVEncoder.processarguments(args)

        self.assertTrue(result.doencode)
        self.assertTrue(result.readonly)

    def test_processarguments_encodereadonlyreverse(self):
        args = []
        args.append(('-l', ''))
        args.append(('-e', ''))
        result = TVEncoder.processarguments(args)

        self.assertTrue(result.doencode)
        self.assertTrue(result.readonly)

    def test_processarguments_encode(self):
        args = []
        args.append(('-e', ''))
        result = TVEncoder.processarguments(args)

        self.assertTrue(result.doencode)
        self.assertFalse(result.readonly)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TVEncoderTest)
    unittest.TextTestRunner(verbosity=2).run(suite)