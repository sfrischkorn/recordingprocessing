# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:10:47 2013

@author: shanef
"""

import MySQLdb as mdb
from libtvshow import TVShow

class MythTV:
    def __init__(self, settings):
        self.settings = settings
        
    def RetrieveEpisodeData(self, inputFile):
        con = mdb.connect(self.settings.MythTVAddress(), self.settings.MythTVUser(), self.settings.MythTVPassword(), self.settings.MythTVDatabase())
            
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select episode, season, title, subtitle, description from mythconverg.recorded where basename = '{0}'".format(inputFile))
            result = cur.fetchone()
            #print result
                
            return TVShow(result['episode'], result['season'], result['title'], result['subtitle'], result['description'])
    
    def FixMythTVEpisodeName(self, showName, episodeTitle):
        for prefix in self.settings.GetShowMythTVEpisodePrefix(showName):
            if episodeTitle.lower().startswith(prefix.lower()):
                return episodeTitle[len(prefix):]
        
        return episodeTitle #didn't find anything so return the episode title
      