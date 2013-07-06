# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:14:22 2013

@author: shanef
"""

import sys
import getopt
import libfilemanager
from libsettings import Settings
from libhandbrake import Encoder
import libtvdatasource

TVRECORDINGSDIR = "/Volumes/TV Recordings/"
#TVRECORDINGSDIR = "/srv/storage2/videos/TVRecordings/" # TODO move this to settings

def ShowHelp():
    print 'TVEncoder.py -p -n <number of files to prepare for processing> - prepare n recordings'
    print 'TVEncoder.py -p -l -n <number of files to process> - lists the files that will be processed without actually encoding them'
    print 'TVEncoder.py -e - encode the files that have been processed'
    print 'TVEncoder.py -e -l - list the files that would be encoded'

def PrintShowsToEncode(showData):
    print "/n".join(showData)

def PrintShowsToPrepare(showsData):
    for showData in showsData:
        showData.Print()

def main(argv):
    numFiles = 0
    doEncode = False
    readOnly = True
    doList = False
    
    try:
       opts, args = getopt.getopt(argv,"hlpen:")
    except getopt.GetoptError:
       ShowHelp()
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          ShowHelp()
          sys.exit()
       elif opt == "-p":
           doEncode = False
           readOnly = False
       elif opt == "-e":
           readOnly = False
           doEncode = True
       elif opt == "-n":
          numFiles = arg
       elif opt == "-l":
          readOnly = True
          doList = True
    
    showSettings = Settings("settings.xml") # TODO call actual settings file

    if readOnly and doList:
        if doEncode:
            #Generate the list of files that would be encoded
            showData = libfilemanager.GetEncodingFiles(showSettings, readOnly)
            PrintShowsToEncode(showData)
        else:
            # Generate the list of files to process
            tempShowList = ["Thomas and Friends", "Thomas the Tank Engine & Friends", 
                            "Chuggington", "Mike the Knight", "Octonauts", 
                            "The Octonauts", "In the Night Garden", 
                            "Raa Raa! The Noisy Lion"] # TODO get from settings
            shows = libfilemanager.GetFilesToPrepare(TVRECORDINGSDIR, numFiles, tempShowList)
            print "num results: {0}".format(len(shows))
            PrintShowsToPrepare(shows)
    else:
        if doEncode:
            #Encode the files and move them to their final destination
            showData = libfilemanager.GetEncodingFiles(shows, readOnly)
            
            for show in showData:
                if libfilemanager.CheckFileExists(show.outputFile):
                    print "File {0} already exists. Cannot process.".format(show.outputFile)
                else:
                    result = Encoder.Encode(show.inputFile, show.outputFile)
                    
                    libfilemanager.PerformPostEncodeFileOperations(show.inputFile, show.outputFile)
        else:
            # TODO Process files for encoding
            shows = libfilemanager.GetFilesToPrepare(TVRECORDINGSDIR, numFiles, shows)
            libtvdatasource.PrepareEpisodes(shows)

if __name__ == "__main__":
    main(sys.argv[1:])