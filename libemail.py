# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 20:48:10 2013

@author: shanef
"""

from libsettings import EmailSettings

import smtplib
from email.mime.text import MIMEText


def sendemail(settingsfilename, subject, body):
    """
    Send an email using the settings defined in settingsfilename
    """

    settings = EmailSettings(settingsfilename)

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = settings.getfromaddress()
    msg["To"] = settings.gettoaddress()

    smtp = smtplib.SMTP(settings.getsmtpserver())
    smtp.ehlo()
    smtp.starttls()
    smtp.login(settings.getsmtpuser(), settings.getsmtppassword())
    smtp.sendmail(settings.getfromaddress(), [settings.gettoaddress()],
                  msg.as_string())
    smtp.quit()
