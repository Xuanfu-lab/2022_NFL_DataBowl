import pandas as pd
from math import isnan

from PlaysAnalysis import uniquePlayID
from PlayerAnalysis import PlayerAnalysis, PFFMalfunction

fileName = 'rawData/PFFScoutingData.csv'

class ScountingAnalysis:
    def __init__(self, fileName):
        self.fileName = fileName


    def readRawData(self):
        rawData = pd.read_csv(self.fileName)
        return rawData

    def tacklerInfo(self, playIDList):
        playerInfo = PlayerAnalysis()
        getPlayerID = playerInfo.getPlayerIDFromAbbr
        def getTacklerHelper(row, i, success):
            if isinstance(row[i], float):
                return []
            else:
                result = []
                for abbr in row[i].split('; '):
                    try:
                        result.append((getPlayerID(row[1], abbr), success))
                    except PFFMalfunction:
                        continue
                return result

        rawData = self.readRawData()
        tacklerDict = {}
        for row in rawData.itertuples(name=None):
            playID = uniquePlayID(row[1], row[2])
            if playID in playIDList:
                misTacklers = getTacklerHelper(row, 12, 0)
                assistTacklers = getTacklerHelper(row, 13, 1)
                successTacklers = getTacklerHelper(row, 14, 1)
                tacklers = misTacklers + assistTacklers + successTacklers
                tacklerDict[playID] = tacklers
        return tacklerDict