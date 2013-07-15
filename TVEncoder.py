# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:14:22 2013

@author: shanef
"""

import sys
import getopt
from libfilemanager import FileManager
from libsettings import Settings
import libhandbrake
from libtvdatasource import TVData
from collections import namedtuple
from termcolor import colored


def showhelp():
    """
    Prints the command lines switches that are valid for the program.
    """

    print 'TVEncoder.py -p -n <number of files to prepare for processing> ' \
          '- prepare n recordings'
    print 'TVEncoder.py -p -l -n <number of files to process> - lists the ' \
          'files that will be processed without actually encoding them'
    print 'TVEncoder.py -e - encode the files that have been processed'
    print 'TVEncoder.py -e -l - list the files that would be encoded'


def print_shows(shows):
    """
    Prints he details of the shows.
    """
    okshows = []
    noepisodes = []
    existingfiles = []

    for show in shows:
        showstr = str(show)

        errors = show.checkproblems()
        if not errors:
            okshows.append(showstr)
        elif "NO_EPISODE" in errors:
            noepisodes.append(showstr)
        elif "FILE_EXISTS" in errors:
            existingfiles.append(showstr)

    for show in okshows:
        print show

    if noepisodes:
        print colored("\nDetails of the episode could not be determined for "
                      "the following shows:", 'red')
        for show in noepisodes:
            print colored(show, 'red')

    if existingfiles:
        print colored("\nThe following shows have a pre-existing "
                      "output file:", 'red')
        for show in existingfiles:
            print colored(show, 'red')


def processarguments(options):
    """
    Determine the actions required from the input flags
    """

    inputoptions = namedtuple("inputoptions",
                              "numfiles doencode readonly dolist")

    inputoptions.readonly = False

    for opt, arg in options:
        if opt == '-h':
            showhelp()
            sys.exit()
        elif opt == "-p":
            inputoptions.doencode = False
        elif opt == "-e":
            inputoptions.doencode = True
        elif opt == "-n":
            inputoptions.numfiles = arg
        elif opt == "-l":
            inputoptions.readonly = True

    return inputoptions


def main(argv):
    """
    The main program for TVEncoder.
    """
    try:
        opts, args = getopt.getopt(argv, "hlpen:")
    except getopt.GetoptError:
        showhelp()
        sys.exit(2)
    inputoptions = processarguments(opts)

    settings = Settings("settings.cfg")
    filemanager = FileManager(settings)

    if inputoptions.readonly:
        if inputoptions.doencode:
            #Generate the list of files that would be encoded
            showdata = filemanager.getencodingfiles(inputoptions.readonly)
            print_shows(showdata)
        else:
            # Generate the list of files to process
            shows = filemanager.getfilestoprepare(inputoptions.numfiles)
            print "num results: {0}".format(len(shows))
            print_shows(shows)
    else:
        if inputoptions.doencode:
            #Encode the files and move them to their final destination
            showdata = filemanager.getencodingfiles(inputoptions.readonly)

            for show in showdata:
                if filemanager.checkfileexists(show.outputfile):
                    print "File {0} already exists. Cannot process." \
                        .format(show.outputfile)
                else:
                    result = libhandbrake.encode(settings.handbrakecommand(),
                                                 show.inputfile,
                                                 show.outputfile)
                    # TODO do something with the result
                    filemanager.performpostencodefileoperations(
                        show.inputfile, show.outputfile)
        else:
            # Process files for encoding
            shows = filemanager.getfilestoprepare(inputoptions.numfiles)
            tvdata = TVData(settings)
            tvdata.prepareepisodes(shows)


if __name__ == "__main__":
    main(sys.argv[1:])
