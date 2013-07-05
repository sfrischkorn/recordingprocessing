import os
from xml.etree import ElementTree

SETTINGSFILE = "settings.xml"

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

shows = LoadSettings(SETTINGSFILE)

for show in shows:
    fileList = []
    
    for r,d,f in os.walk(show.inputDirectory):
        for files in f:
            if files.endswith(".mpg"):
                fileList.append(os.path.join(r,files))

    for inputFile in fileList:
        print inputFile
