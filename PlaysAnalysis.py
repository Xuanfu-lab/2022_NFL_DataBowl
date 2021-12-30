import pandas as pd
import json


def uniquePlayID(gameID, playID):
    return gameID + playID * 10000000000


class PlaysAnalysis:
    def __init__(self):
        self.fileName = 'DownsizedData/plays.json'
        self.plays = None


    def getTacklers(self):
        pass


    def getUniquePlay(self, new=False, sourceFileName = None):
        if new:
            print('fetching plays info...')
            playsData = pd.read_csv(sourceFileName)
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
            json.dump(plays, open(self.fileName, 'w'))
            print('finished fetching plays info')
        playsData = json.load(open(self.fileName, 'r'))
        self.plays = {}
        for uid, play in playsData:
            self.plays[int(uid)] = play
        return self.plays

    @staticmethod
    def initialize(fileNames):
        sourceFileName = fileNames['plays']
        PlaysAnalysis().getUniquePlay(new=True, sourceFileName=sourceFileName)

if __name__ == '__main__':
    plays = PlaysAnalysis()
    plays.getUniquePlay(new=True)


