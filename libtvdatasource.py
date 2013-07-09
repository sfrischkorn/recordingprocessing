# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:42:47 2013

@author: shanef
"""

from libmythtv import MythTV
from libsickbeard import Sickbeard
import os
import shutil

# TODO Move these to settings
#PROCESSDIR="/srv/storage2/files/VideoProcessing/"
#THOMAS="Thomas"
#CHUGGINGTON="Chuggington"
#MIKE="MikeTheKnight"
#OCTONAUTS="Octonauts"
#NIGHTGARDEN="InTheNightGarden"
#RAARAA="RaaRaa"
#INPUTDIR="Input"

class TVData:
    def __init__(self, settings):
        self.settings = settings
        
    def FixEpisodeSeasonNumber(self, number):
        if len(number) == 1:
            return "0{0}".format(number)
        else:
            return number
    
    def GetDirectory(self, title, seasonFolder, season, episode):        
        show = self.settings.GetShow(title)
        if not show or show == "":
            print "Couldn't find show for {0}".format(title)
            return self.settings.UnknownDirectory()
        elif season == "S00" or episode == "E00":
            return self.settings.GetShowUnknownDirectory(show)
        else:
            return os.path.join(self.settings.GetShowInputDirectory(show), seasonFolder)
#==============================================================================
#         if title == "Thomas and Friends" or title == "Thomas the Tank Engine & Friends":
#             directory = THOMAS
#         elif title == "Chuggington":
#             directory = CHUGGINGTON
#         elif title == "Mike the Knight":
#             directory = MIKE
#         elif title == "Octonauts" or title == "The Octonauts":
#             directory = OCTONAUTS
#         elif title == "In the Night Garden":
#             directory = NIGHTGARDEN
#         elif title == "Raa Raa! The Noisy Lion":
#             directory = RAARAA
#         else:
#             print "Didn't match"
#==============================================================================
        
#        return os.path.join(PROCESSDIR, directory, INPUTDIR, season)
            
    def RetrieveEpisodeData(self, inputFile):
        file = os.path.basename(inputFile)
        
        mythTv = MythTV(self.settings)
        show = mythTv.RetrieveEpisodeData(file)
        
        showsToProcess = self.settings.GetShowNames(True)
        
        if show.title and show.title in showsToProcess:
            show.title = self.settings.GetShow(show.title)
    
            if (show.season == "0" or show.episode == "0"):
                sickbeard = Sickbeard(self.settings)
                showId = sickbeard.FindShowId(show.title)
                
                if show.subtitle is not None and show.subtitle:
                    show.subtitle = mythTv.FixMythTVEpisodeName(show.title, show.subtitle)
                    show.subtitle = sickbeard.FixEpisodeTitle(show.title, show.subtitle)
                    
                result = sickbeard.FindEpisode(showId, show.subtitle, show.description)
                show.season = str(result[0])
                show.episode = str(result[1])
                show.subtitle = result[2]
            
            if show.subtitle is None or show.subtitle == "":
                show.subtitle = sickbeard.FindEpisodeName(showId, show.season, show.episode)
                
            #if show.season != "0" and show.episode != "0":
            show.season = self.FixEpisodeSeasonNumber(show.season)
            show.episode = self.FixEpisodeSeasonNumber(show.episode)
            
            seasonFolder = "Season {0}".format(show.season)
            season = "S{0}".format(show.season)
            episode = "E{0}".format(show.episode)
            renamedFile = "{0}{1} - {2} - SD TV_.mpg".format(season, episode, show.subtitle)
                
            directory = self.GetDirectory(show.title, seasonFolder, season, episode)
            
            show.outputFile = os.path.join(directory, file[:-4], renamedFile)
            show.inputFile = inputFile
        
            return show
        else:
            return None
    
#==============================================================================
#     def CheckTitleIsInList(serverAddress, user, password, database, inputFile):
#         """Check that inputFile is a recording of a show that is to be processed."""
#         file = os.path.basename(inputFile)
#         show = MythTV.RetrieveEpisodeData('localhost', 'script', 'script', 'mythconverg', file)
#         
#         # TODO get this from settings
#         if show.title in ["Thomas and Friends", "Thomas the Tank Engine & Friends", 
#                           "Chuggington", "Mike the Knight", "Octonauts", 
#                           "The Octonauts", "In the Night Garden", 
#                           "Raa Raa! The Noisy Lion"]: 
#                               return True
#         else:
#             return False
#==============================================================================
    
    def DetermineTargetFilename(directory, filename, inputFilename):
        dir = os.path.join(directory, inputFilename[:-4])
    	
        if not os.path.exists(dir):
            os.makedirs(dir)
      
        return os.path.join(dir, filename)
        
    
    def ProcessEpisode(self, inputFile, outputFile):  
        outputdir = os.path.dirname(outputFile)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
            
        shutil.copyfile(inputFile, outputFile)
    
    def PrepareEpisodes(self, showsData):
        for showData in showsData:
            self.ProcessEpisode(showData.inputFile, showData.outputFile)