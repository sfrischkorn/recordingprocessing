# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 21:00:35 2013

@author: shane
"""
import json
from urllib import urlopen
from fuzzywuzzy import fuzz
from operator import itemgetter

def FindShowId(showName):
    jsonurl = urlopen("http://192.168.0.2:8081/api/3678177136222bf5002be209220ccb20/?cmd=shows")
    result = json.loads(jsonurl.read())

    shows = []
    for show in result['data']:
        shows.append((show, fuzz.partial_ratio(showName.lower(), result['data'][show]['show_name'].lower())))

    shows = sorted(shows, key=itemgetter(1), reverse=True)

    if shows[0][1] > 85:
        return shows[0][0]

def FindEpisode(showId, name=None, description=None):
    jsonurl = urlopen("http://192.168.0.2:8081/api/3678177136222bf5002be209220ccb20/?cmd=show.seasons&tvdbid={0}".format(showId))
    result = json.loads(jsonurl.read())
    
    for season in result['data']:
        for episode in result['data'][season]:
            if name is not None and name.lower() == result['data'][season][episode]['name'].lower():
                return (season, episode)
            elif description is not None:
                result = FindEpisodeByDescription(showId, season, episode, description)
                if result is not None:
                    return result
    
    return (0, 0)

def GetEpisodeName(subtitle, showName):
    if subtitle[:len(showName)].lower() == showName.lower():
        return subtitle[len(showName + ' and the '):]
    else:
        return subtitle

def FindEpisodeByDescription(showId, season, episode, description):
    jsonEpisodeUrl = urlopen("http://192.168.0.2:8081/api/3678177136222bf5002be209220ccb20/?cmd=episode&tvdbid={0}&season={1}&episode={2}".format(showId, season, episode))
    episodeResult = json.loads(jsonEpisodeUrl.read())

    if fuzz.ratio(episodeResult['data']['description'].lower(), description.lower()) > 85:
        return (season, episode)
    
    return None
        
showId = FindShowId('Mike the Knight')
#showId = FindShowId("Octonauts")
#print showId

subtitle = 'Mike the Knight and the Knightly Campout'

description = "When the Octopod's waterworks are flooded with frightened Humuhumu fish, the Octonauts have to find a way to flush them out!"

episodeName = GetEpisodeName(subtitle, 'Mike the Knight')

result = FindEpisode(showId, episodeName)
#result = FindEpisodeByDescription(showId, description)
print result[0]
print result[1]