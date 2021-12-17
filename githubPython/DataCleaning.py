import pandas as pd
from time import time
from tqdm import tqdm
import json, codecs
import csv

uniquePlayFileName = 'DownsizedData/uniquePlays.json'


def loadData(rawFilename: str, largeFile=False, nrows: int = None) -> pd.DataFrame:
    filename = 'rawData/' + rawFilename
    if not largeFile:
        return pd.read_csv(filename)
    if nrows is None:
        return pd.read_csv(open(filename, 'r'))
    else:
        return pd.read_csv(filename, nrows=nrows)


def uniquePlayID(gameID, playID):
    return gameID + playID * 10000000000


class DataCleaning:
    def __init__(self, year: int, nrows: int = None):
        if year not in [2018, 2019, 2020]:
            raise ValueError(f'wrong year: input was {str(year)}')
        self.trackingFileName = f'tracking{str(year)}.csv'
        self.nrows = nrows

        self.plays = None

    def getUniquePlay(self, new=False):
        if new:
            playsData = loadData('plays.csv')
            result = 'Return'
            playtype = ['Punt', 'Kickoff']
            plays = []
            for row in playsData.itertuples(name=None):
                if row[9] == result and row[8] in playtype:
                    # punt = 0, kickoff = 1
                    plays.append([uniquePlayID(row[1], row[2]), [row[11], int(row[8] == 'Kickoff')]])
            json.dump(plays, open(uniquePlayFileName, 'w'))
        t0 = time()
        playsData = json.load(open(uniquePlayFileName, 'r'))
        self.plays = {}
        for uid, play in playsData:
            self.plays[int(uid)] = play
        print(time() - t0)

    def dataDownsizing(self):
        if self.plays is None:
            self.getUniquePlay()
        rawData = loadData(self.trackingFileName, largeFile=True)
        data = []

        # data = [gamePlayID, returnerIndex, type, playerlist, numpyData^)]
        # numpyData = [gameDataAtEachTimeStep]
        # gameDataAtEachTimeStep = [timeFromStart, *ballData, *homeRunPlayerData, *awayPlayerData]
        # homeRunPlayerData = [*playerData]  # awayPlayerData is similar
        t0 = time()
        rowIter = rawData.itertuples(name=None)
        lastRow = None
        while True:
            newRow = next(rowIter)
            if newRow is None:
                break
            playData = None
            playID = uniquePlayID(newRow[16], newRow[17])
            process = playID in self.plays

            if process:
                playData = [playID, *self.plays[playID]]
            n = None
            while True:
                playerID = newRow[10]
                if lastRow is None or lastRow[10] != playerID:
                    n = lastRow[15]
                    for _ in range(22):
                        for _ in range(n):



            while True:
                if process:








        print(time() - t0)
        print(len(processingData))

        # gamesFileName = 'games.csv'
        # playersFileName = 'players.csv'
        # playsFileName = 'plays.csv'
        # PFFFileName = 'PFFScoutingData.csv'
        # self.gamesData = loadData(gamesFileName)
        # self.playersData = loadData(playersFileName)
        # self.playsData = loadData(playsFileName)
        # self.PFFData = loadData(PFFFileName)


if __name__ == '__main__':
    data = DataCleaning(2018, nrows=10)
    # data.getUniquePlay(new=True)
    data.dataDownsizing()

    tracking2018FileName = 'tracking2018.csv'
    tracking2019FileName = 'tracking2019.csv'
    tracking2020FileName = 'tracking2020.csv'

    # time0 = time()

    # a = loadData(tracking2018FileName, largeFile=True, nrows=100)
    # print(time() - time0)

    # print('2018 data read')
    #
    # print('success')
