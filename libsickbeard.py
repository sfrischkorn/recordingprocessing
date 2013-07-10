# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:10:37 2013

@author: shanef
"""

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
        return "http://{0}:{1}/api/{2}/".format(self.__address, self.__port,
                                                self.__apikey)

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
            shows.append((show, fuzz.partial_ratio(showName.lower(),
                                                   result['data'][show]
                                                   ['show_name'].lower())))

        shows = sorted(shows, key=itemgetter(1), reverse=True)

        if shows[0][1] > 85:
            return shows[0][0]

    def FindEpisodeByDescription(self, showId, season, episode, description):
        jsonepisodeurl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}"
                                 "&episode={3}".format(self.__GetApiURL(),
                                 showId, season, episode))
        episoderesult = json.loads(jsonepisodeurl.read())

        sickbearddescription = episoderesult['data']['description']

        if fuzzystringcompare(sickbearddescription, description):
            return (season, episode, episoderesult['data']['name'])

        return None

    def FindEpisodeName(self, showId, season, episode):
        jsonurl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}"
                          "&episode={3}".format(self.__GetApiURL(), showId,
                          int(season), int(episode)))
        result = json.loads(jsonurl.read())
        if result['result'] == 'error':
            return ""
        else:
            return result['data']['name']

    def FindEpisode(self, showId, name=None, description=None):
        jsonurl = urlopen("{0}?cmd=show.seasons&tvdbid={1}".format(
                          self.__GetApiURL(), showId))
        result = json.loads(jsonurl.read())

        for season in result['data']:
            for episode in result['data'][season]:
                episodename = result['data'][season][episode]['name']
                if name is not None and fuzz.partial_ratio(name.lower(),
                                                           episodename) > 90:
                    return (season, episode, episodename)
                elif description is not None:
                    descriptionQueryResult = \
                        self.FindEpisodeByDescription(showId, season,
                                                      episode, description)
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
        sickbeardPrefix = \
            self.__settings.GetShowSickbeardEpisodePrefix(showName)

        if sickbeardPrefix != "":
            if not episodeTitle.lower.startswith(sickbeardPrefix.lower()):
                return "{0} {1}".format(sickbeardPrefix.rstrip(),
                                        episodeTitle.lstrip())

        return episodeTitle


def fuzzystringcompare(string1, string2, matchvalue=85, casesensitive=False):
    """
    Compare two strings to see if they match it first does a straight
    comparison. Secondly, it concatenates the longer string to the length of
    the shorter one, and tries to compare them again.
    """

    if not casesensitive:
        string1 = string1.lower()
        string2 = string2.lower()

    if fuzz.ratio(string1, string2) > matchvalue:
        return True

    if len(string1) > len(string2):
        if fuzz.ratio(string1[:len(string2)], string2) > matchvalue:
            return True
    elif len(string2) > len(string1):
        if fuzz.ratio(string1, string2[:len(string1)]) > matchvalue:
            return True

    return False
