# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:10:37 2013

@author: shanef
"""

from libtvshow import TVShow
import json
from urllib import urlopen
from fuzzywuzzy import fuzz
from operator import itemgetter

class Sickbeard:
    def __init__(self, settings):
        self.__settings = settings
        self.__address = settings.SickbeardAddress()
        self.__port = settings.SickbeardPort()
        self.__apikey = settings.SickbeardAPIKey()
    
    def __GetApiURL(self):
        return "http://{0}:{1}/api/{2}/".format(self.__address, self.__port, self.__apikey)
        
    def FindShowId(self, showName):
        jsonurl = urlopen(self.__GetApiURL()+"?cmd=shows")
        result = json.loads(jsonurl.read())

        # TODO find a better way to do this
        if showName == "Thomas and Friends":
            showName = "Thomas The Tank Engine & Friends"
        elif showName == "The Octonauts":
            showName = "Octonauts"

        shows = []
        for show in result['data']:
            shows.append((show, fuzz.partial_ratio(showName.lower(), result['data'][show]['show_name'].lower())))
    
        shows = sorted(shows, key=itemgetter(1), reverse=True)
    
        if shows[0][1] > 85:
            return shows[0][0]
    
    def FindEpisodeByDescription(self, showId, season, episode, description):
        jsonEpisodeUrl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}&episode={3}".format(self.__GetApiURL(), showId, season, episode))
        episodeResult = json.loads(jsonEpisodeUrl.read())
        
        sickbeardDescription = episodeResult['data']['description']
        if fuzz.ratio(sickbeardDescription.lower(), description.lower()) > 85 or fuzz.ratio(sickbeardDescription.lower()[:len(description)], description.lower()) > 85 or fuzz.ratio(sickbeardDescription.lower(), description.lower()[:len(sickbeardDescription)]) > 85:
            return (season, episode, episodeResult['data']['name'])

        return None

    def FindEpisode(self, showId, name=None, description=None):
        jsonurl = urlopen("{0}?cmd=show.seasons&tvdbid={1}".format(self.__GetApiURL(), showId))
        result = json.loads(jsonurl.read())
        
        for season in result['data']:
            for episode in result['data'][season]:
                if name is not None and fuzz.partial_ratio(name.lower(), result['data'][season][episode]['name'].lower()) > 90:
                    return (season, episode, result['data'][season][episode]['name'])
                elif description is not None:
                    descriptionQueryResult = self.FindEpisodeByDescription(showId, season, episode, description)
                    if descriptionQueryResult is not None:
                        return descriptionQueryResult
        
        return (0, 0, '')
        
#==============================================================================
#     def GetEpisodeName(subtitle, showName):
#         if subtitle[:len(showName)].lower() == showName.lower():
#             return subtitle[len(showName + ' and the '):]
#         else:
#             return subtitle
#==============================================================================
    
    def FixEpisodeTitle(self, showName, episodeTitle):
        sickbeardPrefix = self.__settings.GetShowSickbeardEpisodePrefix(showName)
        if sickbeardPrefix != "":
            if not episodeTitle.lower.startswith(sickbeardPrefix.lower()):
                return "{0} {1}".format(sickbeardPrefix.rstrip(), episodeTitle.lstrip())
        
        return episodeTitle