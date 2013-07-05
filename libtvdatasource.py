# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:42:47 2013

@author: shanef
"""

import libmythtv as MythTV
from libsickbeard import Sickbeard

class TVShow:
    def __init__(self, episode, season, title, subtitle, description, inputFile='', outputFile=''):
        self.episode = episode
        self.season = season
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.inputFile = inputFile
        self.outputFile = outputFile

def FixEpisodeSeasonNumber(number):
    if number < 10:
        return "0{0}".format(number)
    else:
        return str(number)
        
def RetrieveEpisodeData(serverAddress, user, password, database, inputFile, showsToProcess):
    show = MythTV.RetrieveEpisodeData('localhost', 'script', 'script', 'mythconverg', file)
    
    if show.title:
        if show.subtitle:
            show.subtitle = GetEpisodeName(show.subtitle, show.title)

        if (show.season == '0' or show.episode == '0'):
            showId = Sickbeard.FindShowId(show.title)
            
            result = Sickbeard.FindEpisode(showId, show.subtitle, show.description)
            show.season = result[0]
            show.episode = result[1]
            
        if show.season != "0" and show.episode != "0":
            show.season = FixEpisodeSeasonNumber(show.season)
            show.episode = FixEpisodeSeasonNumber(show.episode)
            
            seasonFolder = "Season {0}".format(show.season)
            season = "S{0}".format(show.season)
            episode = "E{0}".format(show.episode)
            renamedFile = "{0}{1} - {2} - SD TV_.mpg".format(season, episode, show.subtitle)
            
            directory = GetDirectory(show.title, seasonFolder)

def CheckTitleIsInList(serverAddress, user, password, database, inputFile):
    """Check that inputFile is a recording of a show that is to be processed."""
    show = MythTV.RetrieveEpisodeData('localhost', 'script', 'script', 'mythconverg', file)
    
    # TODO get this from settings
    if show.title in ["Thomas and Friends", "Thomas the Tank Engine & Friends", 
                      "Chuggington", "Mike the Knight", "Octonauts", 
                      "The Octonauts", "In the Night Garden", 
                      "Raa Raa! The Noisy Lion"]: 
                          return True
    else:
        return False

def GetEpisodeName(subtitle, showName):
    if subtitle[:len(showName)].lower() == showName.lower():
        return subtitle[len(showName + ' and the '):]
    else:
        return subtitle