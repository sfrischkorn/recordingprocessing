# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:26:22 2013

@author: shanef
"""


class TVShow(object):
    """
    Describes the details of a tv episode
    """

    def __init__(self, episode, season, title, subtitle, description,
                 inputfile='', outputfile=''):
        self.episode = str(episode)
        self.season = str(season)
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.inputfile = inputfile
        self.outputfile = outputfile

    def __str__(self):
        return "Input: {0} -> Output: {1}".format(self.inputfile,
                                                  self.outputfile)
