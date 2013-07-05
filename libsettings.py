# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 20:14:15 2013

@author: shanef
"""

from libtvdatasource import TVShow
from xml.etree import ElementTree

class Settings:
    def __init__(self, settingsFile):
        self.shows = self.LoadSettings(settingsFile)
    
    def LoadSettings(source):
        shows = []
        settingsXml = ElementTree.parse(source).getroot()

        for show in settingsXml.findall('show'):     
            newShow = TVShow(show[0].text, show[1].text, show[2].text)
            shows.append(newShow)
        return shows