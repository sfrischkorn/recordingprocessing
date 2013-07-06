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
    def __init__(self, address, port, apikey):
        self.address = address
        self.port = port
        self.apikey = apikey
    
    def __GetApiURL(self):
        return "http://{0}:{1}/api/{2}/".format(self.address, self.port, self.apikey)
        
    def FindShowId(self, showName):
        jsonurl = urlopen(self.__GetApiURL()+"?cmd=shows")
        result = json.loads(jsonurl.read())

        shows = []
        for show in result['data']:
            shows.append((show, fuzz.partial_ratio(showName.lower(), result['data'][show]['show_name'].lower())))
    
        shows = sorted(shows, key=itemgetter(1), reverse=True)
    
        if shows[0][1] > 85:
            return shows[0][0]
    
    def FindEpisodeByDescription(self, showId, season, episode, description):
        jsonEpisodeUrl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}&episode={3}".format(self.__GetApiURL(), showId, season, episode))
        episodeResult = json.loads(jsonEpisodeUrl.read())
    
        if fuzz.ratio(episodeResult['data']['description'].lower(), description.lower()) > 85:
            return (season, episode)
        
        return None

    def FindEpisode(self, showId, name=None, description=None):
        jsonurl = urlopen("{0}?cmd=show.seasons&tvdbid={1}".format(self.__GetApiURL(), showId))
        result = json.loads(jsonurl.read())
        
        for season in result['data']:
            for episode in result['data'][season]:
                if name is not None and name.lower() == result['data'][season][episode]['name'].lower():
                    return (season, episode)
                elif description is not None:
                    result = self.FindEpisodeByDescription(showId, season, episode, description)
                    if result is not None:
                        return result
        
        return (0, 0)
        
    def GetEpisodeName(subtitle, showName):
        if subtitle[:len(showName)].lower() == showName.lower():
            return subtitle[len(showName + ' and the '):]
        else:
            return subtitle