# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 23:31:16 2013

@author: shanef
"""

from minimock import Mock, mock
import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import libemail
from libsettings import EmailSettings
import smtplib


class libemailtest(unittest.TestCase):
    def test_SendEmail(self):
        mock("EmailSettings.getfromaddress", returns="from@email.com")
        mock("EmailSettings.gettoaddress", returns="to@email.com")
        mock("EmailSettings.getsmtpserver", returns="smtp.test")
        mock("EmailSettings.getsmtpuser", returns="user")
        mock("EmailSettings.getsmtppassword", returns="password")
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

        libemail.sendemail("test", "subject", "body")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(libemailtest)
    unittest.TextTestRunner(verbosity=2).run(suite)
