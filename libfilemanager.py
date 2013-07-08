# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:11:31 2013

@author: shanef
"""

import glob
from libtvdatasource import TVData
import os
import shutil

#move this to settings
#TVRECORDINGSDIR = "/srv/storage2/videos/TVRecordings/"

class EncodeData:
    inputFile = ''
    show = None
    outputFile = ''
    
    def ToString(self):
        return "Input: {0}/tOutput: {2}".format(self.inputFile, self.outputFile)

class FileManager:
    def __init__(self, settings):
        self.settings = settings
        
    def __GetInputFilesToEncode(self):
        fileList = []
        
        for show in self.settings.GetShowNames():
            for r,d,f in os.walk(show.GetShowInputDirectory(show)):
                for files in f:
                    if files.endswith(".mpg"):
                        data = EncodeData()
                        data.show = show
                        data.inputFile = os.path.join(r,files)
                        fileList.append(data)
        
        return fileList
    
    def __FindSeason(self, path, fileName, readOnly):
        season = "Season {0}".format(fileName[1:3])
        seasonPath = os.path.join(path, season)
    
        if not readOnly:    
            if not os.path.exists(seasonPath):
                os.makedirs(seasonPath)
        
        return seasonPath
    
    def __GetEncodeOutputFile(self, inputFile, showName, readOnly):
        inFile = os.path.basename(inputFile)
        outFilename = inFile[:-3]+"mkv"
        outPath = self.__FindSeason(self.settings.GetShowOutputFile(showName), outFilename)
        return os.path.join(outPath, outFilename)
    
    def GetEncodingFiles(self, readOnly=True):
        showsData = self.__GetInputFilesToEncode(self.settings.GetShowNames())
        for showData in showsData:
            showData.outputFile = self.__GetEncodeOutputFile(showData.inputFile, showData.name, readOnly)
        
        return showsData
    
    def CheckFileExists(self, file):
        return os.path.isfile(file)
        
    def __GetRecordingFile(self, fileName):
        return os.path.join(self.settings.TVRecordingDirectory, os.path.dirname(fileName).split("/")[-1] + ".mpg")
        
    def PerformPostEncodeFileOperations(self, inputFileName, outputFileName):
        shutil.rmtree(os.path.dirname(inputFileName))
    
        linkAddress = self.__GetRecordingFile(inputFileName)
    
        os.remove(linkAddress)
    
        os.symlink(outputFileName, linkAddress)
    
    def GetFilesToPrepare(self, numberofFiles):
        path = self.settings.TVRecordingDirectory()
        files = glob.glob("{0}*.mpg".format(path))
        files = sorted(files, key=os.path.getctime)
        files = filter(lambda file: not os.path.islink(file), files)
        
        #files is now a list of unprocessed files, but contains shows other than those we are interested in  
        
        showsToProcess = []
        i = 0
        print "Found {0} potential files".format(len(files))

        tvData = TVData(self.settings)        
        
        for file in files:
            # TODO get these from settings
            #if TVData.CheckTitleIsInList('localhost', 'script', 'script', 'mythconverg', file):
            showData = tvData.RetrieveEpisodeData(file)
            if showData:
                showsToProcess.append(showData)
                i = i + 1
                if i == int(numberofFiles):
                    return showsToProcess
        
        return showsToProcess #will reach here if there were less than numberofFiles found
    