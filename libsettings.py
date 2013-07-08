# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 20:14:15 2013

@author: shanef
"""

from configobj import ConfigObj

class ShowSettings:
    def __init__(self, name, inputDirectory, outputDirectory):
        self.name = name
        self.inputDirectory = inputDirectory
        self.outputDirectory = outputDirectory


class Settings:
    def __init__(self, settingsFile):
        self.__config = ConfigObj(settingsFile)
    
    def TVRecordingDirectory(self):
        return self.__config["TVRecordings"]

    def HandbrakeCommand(self):
        return self.__config["HandbrakeCommand"]
        
    def MythTVAddress(self):
        return self.__config["MythTV"]["address"]
    
    def MythTVUser(self):
        return self.__config["MythTV"]["user"]        

    def MythTVPassword(self):
        return self.__config["MythTV"]["password"]

    def MythTVDatabase(self):
        return self.__config["MythTV"]["database"]
        
    def SickbeardAddress(self):
        return self.__config["Sickbeard"]["address"]
        
    def SickbeardPort(self):
        return int(self.__config["Sickbeard"]["port"])

    def SickbeardAPIKey(self):
        return self.__config["Sickbeard"]["APIKey"]
    
    def UnknownDirectory(self):
        return self.__config["Shows"]["UnknownInput"]
    
    def GetShowNames(self, includeAlias=False):
        shows = self.__config["Shows"].sections
        result = shows[:]
        if includeAlias:
            for show in shows:
                for alias in self.__config["Shows"][show]["alias"]:
                    result.append(alias)
        return result
    
    def GetShowInputDirectory(self, showName):
        show = self.__GetShowSubsection(showName)
        if show is None:
            return ""
        else:
            return show["InputDirectory"]
    
    def GetShowOutputDirectory(self, showName):
        show = self.__GetShowSubsection(showName)
        if show is None:
            return ""
        else:
            return show["OutputDirectory"]
    
    def GetShowAlias(self, showName):
        show = self.__GetShowSubsection(showName)
        if show is None:
            return ""
        else:
            return show["alias"]
    
    def GetShowMythTVEpisodePrefix(self, showName):
        show = self.__GetShowSubsection(showName)
        if show is None:
            return ""
        else:
            return show["MythTvEpisodePrefix"]

    def GetShowSickbeardEpisodePrefix(self, showName):
        show = self.__GetShowSubsection(showName)
        if show is None:
            return ""
        else:
            return show["SickbeardPrefix"]
            
    def GetShow(self, showName):
        showSection = self.__GetShowSubsection(showName)
        if showSection is None:
            return None
        else:
            return showSection.name
    
    def __GetShowSubsection(self, showName):
        if showName in self.GetShowNames():
            return self.__config["Shows"][showName]
        else: # check liases
            for show in self.GetShowNames():
                if showName in self.__config["Shows"][show]["alias"]:
                    return self.__config["Shows"][show]
        
        return None