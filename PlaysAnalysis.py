import pandas as pd
import json

saveFileName = 'DownsizedData/plays.json'

def uniquePlayID(gameID, playID):
    return gameID + playID * 10000000000


class PlaysAnalysis:
    def __init__(self):
        self.plays = None


    def getTacklers(self):
        pass



    def getUniquePlay(self):
        playsData = json.load(open(saveFileName, 'r'))
        self.plays = {}
        for uid, play in playsData:
            self.plays[int(uid)] = play
        return self.plays

    @staticmethod
    def initialize(fileNames):
        print('fetching plays info...')
        sourceName = fileNames['plays']
        playsData = pd.read_csv(sourceName)
        result = 'Return'
        playtype = ['Punt', 'Kickoff']  # [0, 1]
        plays = []
        for row in playsData.itertuples(name=None):
            if row[9] == result and row[8] in playtype:
                # punt = 0, kickoff = 1
                returnerID = None
                try:
                    returnerID = int(row[11])
                except ValueError as err:
                    continue

                plays.append([uniquePlayID(row[1], row[2]), [returnerID, int(row[8] == 'Kickoff')]])
        json.dump(plays, open(saveFileName, 'w'))
        print('finished fetching plays info')

