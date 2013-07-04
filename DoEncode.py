# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 23:25:55 2013

@author: shane
"""

import glob
import logging
import os
import shutil
import subprocess
from xml.etree import ElementTree

SETTINGSFILE = "settings.xml"
HANDBRAKECOMMAND = ['HandBrakeCLI', '--verbose', '-i', '"{0}"', '-o', '"{1}"', 
                    '-f', 'mkv', '-e', 'x264', '-x264-preset', 'slower', 
                    '-x264-tune', 'animation', '-q', '20', 
                    '--loose-anamorphic', '--decomb', '--detelecine', 
                    '--denoise="2:1:2:3"', '--deblock']

TVRECORDINGSDIR = "/srv/storage2/videos/TVRecordings/"

LOGFILE = "encoding.log"
ACTIONLOG = "needsAction.log"

class TVShow:
    def __init__(self, name, inputDirectory, outputDirectory):
        self.name = name
        self.inputDirectory = inputDirectory
        self.outputDirectory = outputDirectory

def LoadSettings(source):
    shows = []
    settingsXml = ElementTree.parse(source).getroot()

    for show in settingsXml.findall('show'):     
        newShow = TVShow(show[0].text, show[1].text, show[2].text)
        shows.append(newShow)
    return shows

def FindSeason(path, fileName):
    season = "Season {0}".format(fileName[1:3])
    seasonPath = os.path.join(path, season)
    if not os.path.exists(seasonPath):
        os.makedirs(seasonPath)
    
    return seasonPath

def GetRecordingFile(file):
    return os.path.join(TVRECORDINGSDIR, os.path.dirname(inputFile).split("/")[-1] + ".mpg")

def CheckOldOutputFileExists(file, myLogger):
     myLogger.debug("Searching for existing file: {0}".format(file[:-3]+"*"))
     return glob.glob(file[:-3]+"*")

def CreateLogger(name, filename, level):
     logger = logging.getLogger(name)
     handler = logging.FileHandler(filename)
     formatter = logging.Formatter('%(asctime)s %(message)s')
     handler.setFormatter(formatter)
     handler.setLevel(level)
     logger.addHandler(handler)
     return logger

#generalLogger.basicConfig(filename=LOGFILE, level=logging.DEBUG, format='%(asctime)s %(message)s')

#actionLogger = logging.getLogger("action")
#actionLogger.basicConfig(filename=ACTIONLOG, level=logging.INFO, format='%(asctime)s %(message)s')

logging.basicConfig(level=logging.DEBUG)
generalLogger = CreateLogger("general", LOGFILE, logging.DEBUG)
actionLogger = CreateLogger("action", ACTIONLOG, logging.INFO)

generalLogger.debug("Loading settings from {0}".format(SETTINGSFILE))
shows = LoadSettings(SETTINGSFILE)

for show in shows:
    generalLogger.info("Processing {0}".format(show.name))
    fileList = []
    
    for r,d,f in os.walk(show.inputDirectory):
        for files in f:
            if files.endswith(".mpg"):
                fileList.append(os.path.join(r,files))

    for inputFile in fileList:
        generalLogger.info("Processing file {0}".format(inputFile))
        
        inFile = os.path.basename(inputFile)
        outFilename = inFile[:-3]+"mkv"
        outPath = FindSeason(show.outputDirectory, outFilename)
        outFile = os.path.join(outPath, outFilename)
        generalLogger.debug("Output file is {0}".format(outFile))
        
        if os.path.isfile(outFile):
            message = "File {0} already exists. Not processing any further.".format(outFile)
            generalLogger.warning(message)
            actionLogger.info(message)
        else:
            existingFile = CheckOldOutputFileExists(outFile, generalLogger)
            generalLogger.debug("Search returned {0}".format(existingFile))
            if len(existingFile) > 0:
                message = "There is an existing version of {0} at {1}.".format(outFilename, existingFile[0])
                generalLogger.info(message)
                actionLogger.info(message)
                
            HANDBRAKECOMMAND[3] = inputFile
            HANDBRAKECOMMAND[5] = outFile
            generalLogger.debug("Handbrake command is: {0}".format(HANDBRAKECOMMAND))
            po = subprocess.Popen(HANDBRAKECOMMAND)
            po.wait()
            generalLogger.info("Handbrake completed with return code {0}".format(po.returncode))
            
            generalLogger.info("Deleting input files from {0}".format(os.path.dirname(inputFile)))
            shutil.rmtree(os.path.dirname(inputFile))

            linkAddress = GetRecordingFile(inputFile)
            generalLogger.info("Deleting original file from {0}".format(linkAddress))
            os.remove(linkAddress)

            generalLogger.info("Creating symlink from {0} to {1}".format(linkAddress, outFile))
            os.symlink(outFile, linkAddress)

            generalLogger.info("Processing completed for {0}".format(inputFile))
