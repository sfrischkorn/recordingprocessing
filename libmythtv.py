# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:10:47 2013

@author: shanef
"""

import MySQLdb as mdb
from libtvshow import TVShow

class MythTV:
    def RetrieveEpisodeData(serverAddress, user, password, database, inputFile):
        con = mdb.connect(serverAddress, user, password, database)
        
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select episode, season, title, subtitle, description from mythconverg.recorded where basename = '{0}'".format(inputFile))
            result = cur.fetchone()
            
            return TVShow(result['episode'], result['season'], result['title'], result['subtitle'], result['description'])
      