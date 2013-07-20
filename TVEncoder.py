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
import libemail
from libtvdatasource import TVData
from collections import namedtuple
from termcolor import colored
import logging

SETTINGS = "settings.cfg"
EMAIL_SETTINGS = "EmailSettings.cfg"

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

    settings = Settings(SETTINGS)
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

            logging.basicConfig(level=logging.DEBUG)
            generallogger = createlogger("general", settings.generallogfile(),
                                         logging.DEBUG)
            actionlogger = createlogger("action", settings.actionlogfile(),
                                        logging.INFO)

            showdata = filemanager.getencodingfiles(inputoptions.readonly)
            generallogger.info("There are {0} files to process."
                               .format(len(showdata)))
            for show in showdata:
                generallogger.info("========================================")
                generallogger.info("Processing {0} of {1}, {2}".format(
                    showdata.index(show) + 1, len(showdata), str(show)))

                if filemanager.checkfileexists(show.outputfile):
                    message = "File {0} already exists. Cannot process." \
                              .format(show.outputfile)
                    generallogger.warning(message)
                    actionlogger.warning(message)
                else:
                    result = libhandbrake.encode(settings.handbrakecommand(),
                                                 show.inputfile,
                                                 show.outputfile)

                    generallogger.info("Encode finished with result: {0}"
                                       .format(result))
                    filemanager.performpostencodefileoperations(
                        show.inputfile, show.outputfile)

                    generallogger.info("Processing finished.")
                    generallogger.info("==========================="
                                       "=============\n\n")

            libemail.SendEmail(EMAIL_SETTINGS, "Encoding Complete",
                               "Finished encoding {0} shows."
                               .format(len(showdata)))
        else:
            # Process files for encoding
            shows = filemanager.getfilestoprepare(inputoptions.numfiles)
            print "Preparing {0} files".format(len(shows))
            tvdata = TVData(settings)
            tvdata.prepareepisodes(shows)


def createlogger(name, filename, level):
    """
    Create a logger named <name> that will write to the file <filename>
    """

    logger = logging.getLogger(name)
    handler = logging.FileHandler(filename, mode='w')
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    main(sys.argv[1:])
