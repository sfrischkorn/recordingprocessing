# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:10:47 2013

@author: shanef
"""

import MySQLdb as mdb
from libtvshow import TVShow


class MythTV:
    """
    Contains methods used for interacting with mythtv
    """

    def __init__(self, settings):
        self.__settings = settings

    def retrieveepisodedata(self, inputfile):
        """
        Retrieve the data that mythtv knows about the recorded file.
        """
        con = mdb.connect(self.__settings.mythtvaddress(),
                          self.__settings.mythtvuser(),
                          self.__settings.mythtvpassword(),
                          self.__settings.mythtvdatabase())

        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select episode, season, title, subtitle, "
                        "description from mythconverg.recorded where "
                        "basename = '{0}'".format(inputfile))
            result = cur.fetchone()

            return TVShow(result['episode'], result['season'],
                          result['title'], result['subtitle'],
                          result['description'])

    def fixmythtvepisodename(self, showname, episodetitle):
        """
        Look for any prefixes listed in the configuration file. If there are
        any and the episide title starts with the prefix, remove the prefix
        from the episode title. The searching is done in the order that the
        prefixes are listed in the configuration file.
        """

        for prefix in self.__settings.getshowmythtvepisodeprefix(showname):
            if episodetitle.lower().startswith(prefix.lower()):
                return episodetitle[len(prefix):]

        #didn't find anything so return the episode title
        return episodetitle
