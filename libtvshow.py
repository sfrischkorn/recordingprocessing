# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:26:22 2013

@author: shanef
"""

class TVShow:
    def __init__(self, episode, season, title, subtitle, description, inputFile='', outputFile=''):
        self.episode = episode
        self.season = season
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.inputFile = inputFile
        self.outputFile = outputFile