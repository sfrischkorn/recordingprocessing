# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:42:47 2013

@author: shanef
"""

from libmythtv import MythTV
from libsickbeard import Sickbeard
import os
import shutil


def fixepisodeseasonnumber(number):
    """
    If the number is single digit, return a string with 0 in front of it.
    """

    if len(number) == 1:
        return "0{0}".format(number)
    else:
        return number


class TVData:
    """
    Class contains logic for processing information about tv episodes
    """

    def __init__(self, settings):
        self.__settings = settings

    def getdirectory(self, title, seasonfolder, season, episode):
        """
        Get the directory where prepared episodes will be located.
        """

        show = self.__settings.getshow(title)
        if not show or show == "":
            print "Couldn't find show for {0}".format(title)
            return self.__settings.unknowndirectory()
        elif season == "S00" or episode == "E00":
            return self.__settings.getshowunknowndirectory(show)
        else:
            return os.path.join(self.__settings.getshowinputdirectory(show),
                                seasonfolder)

    def retrieveepisodedata(self, inputfile):
        """
        Retrieve the details of an episode. It first looks up the details that
        mythtv recorded about it, then looks up sickbeard to attempt to find
        any missing details. Finally it determined the output file for it.
        """

        inputfilename = os.path.basename(inputfile)

        mythtv = MythTV(self.__settings)
        show = mythtv.retrieveepisodedata(inputfilename)

        showstoprocess = self.__settings.getshownames(True)

        if show.title and show.title in showstoprocess:
            show.title = self.__settings.getshow(show.title)

            if (show.season == "0" or show.episode == "0"):
                sickbeard = Sickbeard(self.__settings)
                showid = sickbeard.findshowid(show.title)

                if show.subtitle is not None and show.subtitle:
                    show.subtitle = mythtv.fixmythtvepisodename(show.title,
                                                                show.subtitle)
                    show.subtitle = sickbeard.fixepisodetitle(show.title,
                                                              show.subtitle)

                result = sickbeard.findepisode(showid, show.subtitle,
                                               show.description)
                show.season = str(result[0])
                show.episode = str(result[1])
                show.subtitle = result[2]

            if show.subtitle is None or show.subtitle == "":
                show.subtitle = sickbeard.findepisodename(showid, show.season,
                                                          show.episode)

            show.season = fixepisodeseasonnumber(show.season)
            show.episode = fixepisodeseasonnumber(show.episode)

            seasonfolder = "Season {0}".format(show.season)
            season = "S{0}".format(show.season)
            episode = "E{0}".format(show.episode)
            renamedfile = self.getoutputfilename(season, episode,
                                                 show.subtitle)

            directory = self.getdirectory(show.title, seasonfolder,
                                          season, episode)

            show.outputfile = os.path.join(directory, inputfilename[:-4],
                                           renamedfile)
            show.inputfile = inputfile

            return show
        else:
            return None

    def getoutputfilename(self, season, episode, name):
        """
        Get the output filename, and remove any illegal characters
        """

        filename = "{0}{1} - {2} - SD TV_.mpg".format(season, episode, name)

        for illegalcharacter in self.__settings.illegalcharacters():
            filename = filename.replace(illegalcharacter, "")

        return filename

    @staticmethod
    def processepisode(inputfile, outputfile):
        """
        Copy inputfile to outputfile, creating the path for outputfile if
        required.
        """

        outputdir = os.path.dirname(outputfile)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        shutil.copyfile(inputfile, outputfile)

    def prepareepisodes(self, showsdata):
        """
        Copy the files in showsdata from their input directory to their output
        directory.
        """

        for showdata in showsdata:
            print "========================================"
            print "Copying {0} to {1}".format(showdata.inputfile,
                                              showdata.outputfile)

            self.processepisode(showdata.inputfile, showdata.outputfile)

            print "Finished copy"
            print "========================================\n\n"
