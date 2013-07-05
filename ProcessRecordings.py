import os
import shutil
import MySQLdb as mdb
import glob
import json
from urllib import urlopen
from fuzzywuzzy import fuzz
from operator import itemgetter

PROCESSDIR="/srv/storage2/files/VideoProcessing/"
THOMAS="Thomas"
CHUGGINGTON="Chuggington"
MIKE="MikeTheKnight"
OCTONAUTS="Octonauts"
NIGHTGARDEN="InTheNightGarden"
RAARAA="RaaRaa"
INPUTDIR="Input"
SICKBEARDAPI="http://192.168.0.2:8081/api/3678177136222bf5002be209220ccb20/"

class TVShow:
    def __init__(self, episode, season, title, subtitle, description):
        self.episode = episode
        self.season = season
        self.title = title
        self.subtitle = subtitle
        self.description = description

def FindShowId(showName):
    jsonurl = urlopen(SICKBEARDAPI+"?cmd=shows")
    result = json.loads(jsonurl.read())

    shows = []
    for show in result['data']:
        shows.append((show, fuzz.partial_ratio(showName.lower(), result['data'][show]['show_name'].lower())))

    shows = sorted(shows, key=itemgetter(1), reverse=True)

    if shows[0][1] > 85:
        return shows[0][0]

def FindEpisode(showId, name=None, description=None):
    jsonurl = urlopen("{0}?cmd=show.seasons&tvdbid={1}".format(SICKBEARDAPI, showId))
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
    jsonEpisodeUrl = urlopen("{0}?cmd=episode&tvdbid={1}&season={2}&episode={3}".format(SICKBEARDAPI, showId, season, episode))
    episodeResult = json.loads(jsonEpisodeUrl.read())

    if fuzz.ratio(episodeResult['data']['description'].lower(), description.lower()) > 85:
        return (season, episode)
    
    return None

def DetermineTargetFilename(directory, filename, inputFilename):
    dir = os.path.join(directory, inputFilename[:-4])
	
    if not os.path.exists(dir):
        os.makedirs(dir)
  
    return os.path.join(dir, filename)

def ProcessKnownEpisode(directory, filename, inputFilename):
    target = DetermineTargetFilename(directory, filename, inputFilename)
    shutil.move(inputFilename, target)
	
def ProcessUnknownEpisode(inputFilename):
	print "do this"

def RetrieveEpisodeData(inputFile):
    con = mdb.connect('localhost', 'script', 'script', 'mythconverg')
    
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select episode, season, title, subtitle, description from mythconverg.recorded where basename = '{0}'".format(inputFile))
        result = cur.fetchone()
        
        return TVShow(result['episode'], result['season'], result['title'], result['subtitle'], result['description'])
    
def FixEpisodeSeasonNumber(number):
    if number < 10:
        return "0{0}".format(number)
    else:
        return str(number)

def GetDirectory(title, season):
    directory = ""
    if title == "Thomas and Friends" or title == "Thomas the Tank Engine & Friends":
        directory = THOMAS
    elif title == "Chuggington":
        directory = CHUGGINGTON
    elif title == "Mike the Knight":
        directory = MIKE
    elif title == "Octonauts" or title == "The Octonauts":
        directory = OCTONAUTS
    elif title == "In the Night Garden":
        directory = NIGHTGARDEN
    elif title == "Raa Raa! The Noisy Lion":
        directory = RAARAA
    else:
        print "Didn't match"
    
    return os.path.join(PROCESSDIR, directory, INPUTDIR, season)
    
    
def ProcessEpisode(inputFile):
    show = RetrieveEpisodeData(inputFile)

    if show.title:
        if show.subtitle:
            show.subtitle = GetEpisodeName(show.subtitle, show.title)

        if (show.season == '0' or show.episode == '0'):
            showId = FindShowId(show.title)
            
            result = FindEpisode(showId, show.subtitle, show.description)
            show.season = result[0]
            show.episode = result[1]
            
        if show.season != "0" and show.episode != "0":
            show.season = FixEpisodeSeasonNumber(show.season)
            show.episode = FixEpisodeSeasonNumber(show.episode)
            
            seasonFolder = "Season {0}".format(show.season)
            season = "S{0}".format(show.season)
            episode = "E{0}".format(show.episode)
            renamedFile = "{0}{1} - {2} - SD TV_.mpg".format(season, episode, show.subtitle)
            
            directory = GetDirectory(show.title, seasonFolder)
            ProcessKnownEpisode(directory, renamedFile, os.path.basename(inputFile))
    else:
        print "no show name"

def GetFilesToProcess():
    return glob.glob("*.mpg")
        
for file in GetFilesToProcess():
    ProcessEpisode(file)
