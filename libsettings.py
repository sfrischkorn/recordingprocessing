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
        """
        Initialise settingsfile as a configobj
        """

        self.__config = ConfigObj(settingsfile)

    def tvrecordingdirectory(self):
        """
        Get the TVRecordings setting
        """

        return self.__config["TVRecordings"]

    def handbrakecommand(self):
        """
        Get the HandbrakeCommand setting
        """

        return self.__config["HandbrakeCommand"]

    def mythtvaddress(self):
        """
        Get the MythTV/address setting
        """

        return self.__config["MythTV"]["address"]

    def mythtvuser(self):
        """
        Get the MythTV/user setting
        """

        return self.__config["MythTV"]["user"]

    def mythtvpassword(self):
        """
        Get the MythTV/password setting
        """

        return self.__config["MythTV"]["password"]

    def mythtvdatabase(self):
        """
        Get the MythTV/database setting
        """

        return self.__config["MythTV"]["database"]

    def sickbeardaddress(self):
        """
        Get the Sickbeard/address setting
        """

        return self.__config["Sickbeard"]["address"]

    def sickbeardport(self):
        """
        Get the Sickbeard/port setting
        """

        return int(self.__config["Sickbeard"]["port"])

    def sickbeardapikey(self):
        """
        Get the Sickbeard/APIKey setting
        """

        return self.__config["Sickbeard"]["APIKey"]

    def unknowndirectory(self):
        """
        Get the Shows/UnknownInput directory. It is the directory used for
        episodes where nothing is known about it
        """

        return self.__config["Shows"]["UnknownInput"]

    def getshownames(self, includealias=False):
        """
        Get a list of the names of the shows that are specified in the
        settings file. If includealias is True, it will also include any
        defined aliases in the list.
        """

        shows = self.__config["Shows"].sections
        result = shows[:]
        if includealias:
            for show in shows:
                for alias in self.__config["Shows"][show]["alias"]:
                    result.append(alias)
        return result

    def findshownameforalias(self, aliasname):
        """
        Find the name of the show. If the supplied aliasname is an alias, it
        will return the show name. If aliasname is the name of a show, it will
        return aliasname
        """

        if aliasname in self.getshownames():
            # aliasname is the name of an actual show
            return aliasname

        # search for the show that the alias belongs to
        for showsettings in self.__config["Shows"]:
            if aliasname in showsettings["alias"]:
                return showsettings.name

        # Could not find it anywhere
        return None

    def getshowinputdirectory(self, showname):
        """
        Get the InputDirectory setting for the show, showname.
        """

        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["InputDirectory"]

    def getshowunknowndirectory(self, showname):
        """
        Get the UnknownDirectory setting for the show, showname. It is used
        when the show is known, but the season or episode are not.
        """

        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["UnknownDirectory"]

    def getshowoutputdirectory(self, showname):
        """
        Get the OutputDirectory setting for the show, showname.
        """

        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["OutputDirectory"]

    def getshowalias(self, showname):
        """
        Get the alias setting for the show, showname. It returns a list of
        aliases.
        """

        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["alias"]

    def getshowmythtvepisodeprefix(self, showname):
        """
        Get the MythTVEpisodePrefix setting for the show, showname.
        """

        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["MythTvEpisodePrefix"]

    def getshowsickbearsepisodeprefix(self, showname):
        """
        Get the SickbeardPrefix setting for the show, showname.
        """

        show = self.__getshowsubsection(showname)
        if show is None:
            return ""
        else:
            return show["SickbeardPrefix"]

    # TODO check if this is actually doing anything. it seems like it
    # just returns what is input
    def getshow(self, showname):
        """
        Get the InputDirectory setting for the show, showname.
        """
        showsection = self.__getshowsubsection(showname)
        if showsection is None:
            return None
        else:
            return showsection.name

    def __getshowsubsection(self, showname):
        """
        Get the configuration options for the show, showname.
        """

        if showname in self.getshownames():
            return self.__config["Shows"][showname]
        else:  # check liases
            for show in self.getshownames():
                if showname in self.__config["Shows"][show]["alias"]:
                    return self.__config["Shows"][show]

        return None
