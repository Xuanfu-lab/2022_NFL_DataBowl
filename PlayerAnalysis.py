import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import json
from math import isnan

playerAbbrFileName = 'AnalyzedData/playerAbbr.json'

class PFFMalfunction(KeyError):
    pass



class PlayerAnalysis:
    def __init__(self, fileNames):
        self.fileName = fileNames['players']
        self.trackingDataFileNames = fileNames['tracking']
        self.gamesDataFileName = fileNames['games']
        self.players = None
        self.playerDict = None

    def getPlayerIDFromAbbr(self, gameID, abbr, jerseyNum=None):
        if self.playerDict is None:
            self.getPlayerAbbr()
        if jerseyNum is None:
            abbr, jerseyNum = abbr.split()
            jerseyNum = int(jerseyNum)
        try:
            return self.playerDict[gameID][abbr][jerseyNum]
        except KeyError as err:
            if jerseyNum == 47:
                jerseyNum = 46
            elif jerseyNum == 38:
                raise PFFMalfunction()
            else:
                raise
            return self.playerDict[gameID][abbr][jerseyNum]




    def getPlayerAbbr(self, new=False):
        if new:
            print('building player abbr dictionary...')
            dataFromTracking = defaultdict(lambda: defaultdict(dict))
            oldPlayerID = None
            for trackingDataFileName in self.trackingDataFileNames:
                trackingData = pd.read_csv(trackingDataFileName)
                for frame in tqdm(trackingData.itertuples(name=None)):
                    playerID = frame[10]
                    if playerID != oldPlayerID:
                        oldPlayerID = playerID
                        if playerID is None:
                            continue
                        if isnan(playerID):
                            continue
                        playerID = int(playerID)
                        gameID = int(frame[16])
                        team = frame[14]
                        jerseyNum = int(frame[12])
                        dataFromTracking[gameID][team][jerseyNum] = playerID

            teamInfo = {}
            gamesFile = self.gamesDataFileName
            gamesData = pd.read_csv(open(gamesFile))
            for game in tqdm(gamesData.itertuples(name=None)):
                gameID = int(game[1])
                teamInfo[gameID] = [*game[6:8]]
            for gameID in tqdm(dataFromTracking):
                homeAwayData = dataFromTracking[gameID]
                teamAbbr = teamInfo[gameID]
                teamData = {teamAbbr[0]: homeAwayData['home'], teamAbbr[1]: homeAwayData['away']}
                dataFromTracking[gameID] = teamData
            json.dump(dataFromTracking, open(playerAbbrFileName, 'w'))
            self.playerDict = dataFromTracking
        else:
            playerDictList = json.load(open(playerAbbrFileName, 'r'))
            playerDict = {
                int(gameID): {teamAbbr: {int(jerseyNum): playerID for jerseyNum, playerID in players.items()} for
                              teamAbbr, players in game.items()} for gameID, game in playerDictList.items()}
            self.playerDict = playerDict
        return self.playerDict

    @staticmethod
    def initialize(fileNames):
        PlayerAnalysis(fileNames).getPlayerAbbr(new=True)



if __name__ == "__main__":
    playerInfo = PlayerAnalysis()
    playerInfo.getPlayerAbbr()
    print(len(playerInfo.playerDict))
    print(playerInfo.getPlayerIDFromAbbr(2018123000, 'BAL 26'))