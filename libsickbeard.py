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
    """
    Contains operations used to interact with sickbeard
    """

    def __init__(self, settings):
        self.__settings = settings
        self.__address = settings.sickbeardaddress()
        self.__port = settings.sickbeardport()
        self.__apikey = settings.sickbeardapikey()

    def findshowid(self, showname):
        """
        Get the tvdb show id for the show
        """

        jsonurl = urlopen(self.__getapiurl()+"?cmd=shows")
        result = json.loads(jsonurl.read())

        showname = self.__settings.findshownameforalias(showname)

        shows = []
        for show in result['data']:
            shows.append((show, fuzz.partial_ratio(showname.lower(),
                                                   result['data'][show]
                                                   ['show_name'].lower())))

        shows = sorted(shows, key=itemgetter(1), reverse=True)

        if shows[0][1] > 85:
            return shows[0][0]

    def findepisodename(self, showid, season, episode):
        """
        Get the name of an episode, given it's season and episode numbers
        """

        jsonurl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}"
                          "&episode={3}".format(self.__getapiurl(), showid,
                                                int(season), int(episode)))

        result = json.loads(jsonurl.read())

        if result['result'] == 'error':
            return ""
        else:
            return result['data']['name']

    def findepisode(self, showid, name=None, description=None):
        """
        Find an episode, either by it's name or it's description. This is used
        when the season and episode numbers are not known
        """

        jsonurl = urlopen("{0}?cmd=show.seasons&tvdbid={1}".format(
                          self.__getapiurl(), showid))

        result = json.loads(jsonurl.read())

        for season in result['data']:
            for episode in result['data'][season]:
                episodename = result['data'][season][episode]['name']
                if name is not None and fuzz.ratio(name.lower(),
                                                   episodename.lower()) > 85:
                    return (season, episode, episodename)
                elif description is not None:
                    descriptionqueryresult = \
                        self.__findepisodebydescription(showid, season,
                                                        episode, description)
                    if descriptionqueryresult is not None:
                        return descriptionqueryresult

        return (0, 0, '')

    def fixepisodetitle(self, showname, episodetitle):
        """
        Check to see if there is a prefix specified for the show. If there is,
        add the prefix to the start of the episode title
        """

        sickbeardprefix = \
            self.__settings.getshowsickbeardepisodeprefix(showname)

        if sickbeardprefix != "":
            if not episodetitle.lower().startswith(sickbeardprefix.lower()):
                return "{0} {1}".format(sickbeardprefix.rstrip(),
                                        episodetitle.lstrip())

        return episodetitle

    def __getapiurl(self):
        """
        Get the url of the sickbeard api, substituting the values from the
        settings
        """

        return "http://{0}:{1}/api/{2}/".format(self.__address, self.__port,
                                                self.__apikey)

    def __findepisodebydescription(self, showid, season, episode, description):
        """
        Find the details of an episode by searching for it's description
        """

        jsonepisodeurl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}"
                                 "&episode={3}".format(self.__getapiurl(),
                                                       showid, season,
                                                       episode))
        episoderesult = json.loads(jsonepisodeurl.read())

        sickbearddescription = episoderesult['data']['description']

        if fuzzystringcompare(sickbearddescription, description):
            return (season, episode, episoderesult['data']['name'])

        return None


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
