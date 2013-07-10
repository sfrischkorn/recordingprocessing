# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 20:14:15 2013

@author: shanef
"""

from configobj import ConfigObj


#==============================================================================
# class ShowSettings:
#     """
#     Container for the settings for a show
#     """
#
#     def __init__(self, name, inputdirectory, outputdirectory):
#         self.name = name
#         self.inputdirectory = inputdirectory
#         self.outputdirectory = outputdirectory
#==============================================================================


class Settings:
    """
    Accessor for the configuration file
    """

    def __init__(self, settingsfile):
        self.__config = ConfigObj(settingsfile)

    def tvrecordingdirectory(self):
        return self.__config["TVRecordings"]

    def handbrakecommand(self):
        return self.__config["HandbrakeCommand"]

    def mythtvaddress(self):
        return self.__config["MythTV"]["address"]

    def mythtvuser(self):
        return self.__config["MythTV"]["user"]

    def mythtvpassword(self):
        return self.__config["MythTV"]["password"]

    def mythtvdatabase(self):
        return self.__config["MythTV"]["database"]

    def sickbeardaddress(self):
        return self.__config["Sickbeard"]["address"]

    def sickbeardport(self):
        return int(self.__config["Sickbeard"]["port"])

    def sickbeardapikey(self):
        return self.__config["Sickbeard"]["APIKey"]

    def unknowndirectory(self):
        return self.__config["Shows"]["UnknownInput"]

    def getshownames(self, includealias=False):
        shows = self.__config["Shows"].sections
        result = shows[:]
        if includealias:
            for show in shows:
                for alias in self.__config["Shows"][show]["alias"]:
                    result.append(alias)
        return result

    def getshowinputdirectory(self, showname):
        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["InputDirectory"]

    def getshowunknowndirectory(self, showname):
        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["UnknownDirectory"]

    def getshowoutputdirectory(self, showname):
        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["OutputDirectory"]

    def getshowalias(self, showname):
        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["alias"]

    def getshowmythtvepisodeprefix(self, showname):
        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["MythTvEpisodePrefix"]

    def getshowsickbearsepisodeprefix(self, showname):
        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["SickbeardPrefix"]

    def getshow(self, showname):
        showsection = self.__getshowsubsection(showname)
        if showsection is None:
            return None
        else:
            return showsection.name

    def __getshowsubsection(self, showname):
        if showname in self.getshownames():
            return self.__config["Shows"][showname]
        else:  # check liases
            for show in self.getshownames():
                if showname in self.__config["Shows"][show]["alias"]:
                    return self.__config["Shows"][show]

        return None
