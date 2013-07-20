# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 20:48:10 2013

@author: shanef
"""

from libsettings import EmailSettings

import smtplib
from email.mime.text import MIMEText


def sendemail(settingsfilename, subject, body):
    settings = EmailSettings(settingsfilename)

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = settings.getfromaddress()
    msg["To"] = settings.gettoaddress()

    s = smtplib.SMTP(settings.getsmtpserver())
    s.ehlo()
    s.starttls()
    s.login(settings.getsmtpuser(), settings.getsmtppassword())
    s.sendmail(settings.getfromaddress(), [settings.gettoaddress()],
               msg.as_string())
    s.quit()
