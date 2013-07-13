# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:11:31 2013

@author: shanef
"""

import glob
from libtvdatasource import TVData
import os
import shutil


class EncodeData:
    """
    Contains detais of files to encode.
    inputfile - The source file
    outputfile - The destination file
    show - The name of the show
    """

    def __init__(self, inputfile='', show=None, outputfile=''):
        self.inputfile = inputfile
        self.show = show
        self.outputfile = outputfile

    def __str__(self):
        return "Show: {0}\nInput: {1}\nOutput: " \
               "{2}\n".format(self.show, self.inputfile, self.outputfile)


class FileManager:
    """
    Perform file operations
    """

    def __init__(self, settings):
        self.__settings = settings

    def getencodingfiles(self, readonly=True):
        """
        Get the details of the shows that are ready for encoding
        """

        showsdata = self.__getinputfilestoencode()
        for showdata in showsdata:
            showdata.outputfile = self.__getencodeoutputfile(
                showdata.inputfile, showdata.show, readonly)

        return showsdata

    def performpostencodefileoperations(self, inputfilename, outputfilename):
        """
        Delete the input file, and the original recorded file. Then create a
        symlink from the new encoded file to the original mythtv file.
        """

        shutil.rmtree(os.path.dirname(inputfilename))

        linkaddress = self.__getrecordingfile(inputfilename)

        os.remove(linkaddress)

        os.symlink(outputfilename, linkaddress)

    def getfilestoprepare(self, numberoffiles):
        """
        Get the details of the first <numberoffiles> to prepare for encoding.
        If there are less files than <numberoffiles> available, it will
        return the details of the number available.
        """

        path = self.__settings.tvrecordingdirectory()
        potentialfiles = glob.glob("{0}*.mpg".format(path))
        potentialfiles = sorted(potentialfiles, key=os.path.getctime)
        potentialfiles = [potentialfile for potentialfile in potentialfiles
                          if not os.path.islink(potentialfile)]

        #files is now a list of unprocessed files, but contains shows other
        #than those we are interested in
        showstoprocess = []
        i = 0
        print "Found {0} potential files".format(len(potentialfiles))

        tvdata = TVData(self.__settings)

        for potentialfile in potentialfiles:
            showdata = tvdata.retrieveepisodedata(potentialfile)
            if showdata:
                showstoprocess.append(showdata)
                i = i + 1
                if i == int(numberoffiles):
                    return showstoprocess

        #will reach here if there were less than numberofFiles found
        return showstoprocess

    @staticmethod
    def checkfileexists(filename):
        """
        Check to see if a file currently exists
        """

        return os.path.exists(filename)

    def __getinputfilestoencode(self):
        """
        Get the details of the files that are waiting to be encoded
        """

        filelist = []

        for show in self.__settings.getshownames():
            for dirpath, dirnames, filenames in os.walk(
                    self.__settings.getshowinputdirectory(show)):
                for inputfile in filenames:
                    if inputfile.endswith(".mpg"):
                        data = EncodeData(show, os.path.join(
                            dirpath, inputfile))
                        filelist.append(data)

        return filelist

    def __getencodeoutputfile(self, inputfile, showname, readonly):
        """
        Get the full path of the output filename to save the encoded video to
        """

        infile = os.path.basename(inputfile)
        outfilename = infile[:-3]+"mkv"
        outpath = findseason(self.__settings.getshowoutputdirectory(
            showname), outfilename, readonly)
        return os.path.join(outpath, outfilename)

    def __getrecordingfile(self, filename):
        """
        Get the name of the mythtv recording based on the filename. The
        filename contains the name of the mythtv recording as the
        final directory in it's path.
        """

        return os.path.join(self.__settings.TVRecordingDirectory(),
                            os.path.dirname(filename).split("/")[-1] + ".mpg")


def findseason(path, filename, readonly):
    """
    Get the name of the season folder. eg. Season 01
    """

    season = "Season {0}".format(filename[1:3])
    seasonpath = os.path.join(path, season)

    if not readonly:
        if not os.path.exists(seasonpath):
            os.makedirs(seasonpath)

    return seasonpath
