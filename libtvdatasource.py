# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:42:47 2013

@author: shanef
"""

import libmythtv as MythTV
from libsickbeard import Sickbeard
import os
import shutil

# TODO Move these to settings
PROCESSDIR="/srv/storage2/files/VideoProcessing/"
THOMAS="Thomas"
CHUGGINGTON="Chuggington"
MIKE="MikeTheKnight"
OCTONAUTS="Octonauts"
NIGHTGARDEN="InTheNightGarden"
RAARAA="RaaRaa"
INPUTDIR="Input"

def FixEpisodeSeasonNumber(number):
    if number < 10:
        return "0{0}".format(number)
    else:
        return str(number)

def GetDirectory(title, season):
    directory = ""
    if title == "Thomas and Friends" or title == "Thomas the Tank Engine & Friends":
        directory = THOMAS
    elif title == "Chuggington":
        directory = CHUGGINGTON
    elif title == "Mike the Knight":
        directory = MIKE
    elif title == "Octonauts" or title == "The Octonauts":
        directory = OCTONAUTS
    elif title == "In the Night Garden":
        directory = NIGHTGARDEN
    elif title == "Raa Raa! The Noisy Lion":
        directory = RAARAA
    else:
        print "Didn't match"
    
    return os.path.join(PROCESSDIR, directory, INPUTDIR, season)
        
def RetrieveEpisodeData(serverAddress, user, password, database, inputFile, showsToProcess, sickbeardAddress, sickbeardPort, sickbeardAPIKey):
    file = os.path.basename(inputFile)
    show = MythTV.RetrieveEpisodeData(serverAddress, user, password, database, file)
    print show
    if show.title and show.title in showsToProcess:
        if show.subtitle:
            show.subtitle = GetEpisodeName(show.subtitle, show.title)

        if (show.season == '0' or show.episode == '0'):
            sickbeard = Sickbeard(sickbeardAddress, sickbeardPort, sickbeardAPIKey)
            showId = sickbeard.FindShowId(show.title)
            
            result = sickbeard.FindEpisode(showId, show.subtitle, show.description)
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
            
            show.outputFile = os.path.join(directory, inputFile[:-4], renamedFile)
            show.inputFile = inputFile
    
        return show
    else:
        return None

def CheckTitleIsInList(serverAddress, user, password, database, inputFile):
    """Check that inputFile is a recording of a show that is to be processed."""
    file = os.path.basename(inputFile)
    show = MythTV.RetrieveEpisodeData('localhost', 'script', 'script', 'mythconverg', file)
    
    # TODO get this from settings
    if show.title in ["Thomas and Friends", "Thomas the Tank Engine & Friends", 
                      "Chuggington", "Mike the Knight", "Octonauts", 
                      "The Octonauts", "In the Night Garden", 
                      "Raa Raa! The Noisy Lion"]: 
                          return True
    else:
        return False

def DetermineTargetFilename(directory, filename, inputFilename):
    dir = os.path.join(directory, inputFilename[:-4])
	
    if not os.path.exists(dir):
        os.makedirs(dir)
  
    return os.path.join(dir, filename)
    
def GetEpisodeName(subtitle, showName):
    if subtitle[:len(showName)].lower() == showName.lower():
        return subtitle[len(showName + ' and the '):]
    else:
        return subtitle

def ProcessEpisode(inputFile, outputFile):  
    outputdir = os.path.dirname(outputFile)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        
    shutil.move(inputFile, outputFile)

def PrepareEpisodes(showsData):
    for showData in showsData:
        ProcessEpisode(showData.inputFile, showData.outputFile)