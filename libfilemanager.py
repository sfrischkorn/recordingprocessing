# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:11:31 2013

@author: shanef
"""

import os
import shutil

#move this to settings
TVRECORDINGSDIR = "/srv/storage2/videos/TVRecordings/"

class EncodeData:
    inputFile = ''
    show = None
    outputFile = ''
    
    def ToString():
        return "Input: {0}/tOutput: {2}".format(inputFile, outputFile)

def __GetInputFilesToEncode(shows):
    fileList = []
    
    for show in shows:
        for r,d,f in os.walk(show.inputDirectory):
            for files in f:
                if files.endswith(".mpg"):
                    data = EncodeData()
                    data.show = show
                    data.inputFile = os.path.join(r,files)
                    fileList.append(data)
    
    return fileList

def __FindSeason(path, fileName, readOnly):
    season = "Season {0}".format(fileName[1:3])
    seasonPath = os.path.join(path, season)

    if not readOnly:    
        if not os.path.exists(seasonPath):
            os.makedirs(seasonPath)
    
    return seasonPath

def __GetEncodeOutputFile(showData, readOnly):
    inFile = os.path.basename(showData.inputFile)
    outFilename = inFile[:-3]+"mkv"
    outPath = __FindSeason(showData.show.outputDirectory, outFilename)
    showData.outputFile = os.path.join(outPath, outFilename)
    
    return showData

def GetEncodingFiles(shows, readOnly=True):
    showsData = __GetInputFilesToEncode(shows)
    for showData in showsData:
        showsData = __GetEncodeOutputFile(showData, readOnly)
    
    return showsData

def CheckFileExists(file):
    return os.path.isfile(file)
    
def __GetRecordingFile(fileName):
    return os.path.join(TVRECORDINGSDIR, os.path.dirname(fileName).split("/")[-1] + ".mpg")
    
def PerformPostEncodeFileOperations(inputFileName, outputFileName):
    shutil.rmtree(os.path.dirname(inputFileName))

    linkAddress = __GetRecordingFile(inputFileName)

    os.remove(linkAddress)

    os.symlink(outputFileName, linkAddress)