import pandas as pd
import numpy as np
from time import time
from datetime import datetime
from tqdm import tqdm
import json, codecs
from math import isnan
import csv

uniquePlayFileName = 'DownsizedData/uniquePlays.json'
nan = float('nan')


def loadData(rawFilename: str, nrows: int = None) -> pd.DataFrame:
    filename = 'rawData/' + rawFilename
    if nrows is None:
        return pd.read_csv(filename)
    else:
        return pd.read_csv(filename, nrows=nrows)


def uniquePlayID(gameID, playID):
    return gameID + playID * 10000000000


def getPlayerInfo(row):
    return (int(row[10]), row[14] == 'home', int(row[12]))


def getPlayerData(row):
    return [row[2], row[3], row[4], row[5], row[6], row[7], row[8]]


def getBallData(row):
    return [row[2], row[3], row[4], row[5], row[6]]


def transpose(listOfLists: [[]]) -> [[]]:
    n = len(listOfLists[0])

    iterObjs = [iter(i) for i in listOfLists]
    result = []
    try:
        for _ in range(n):
            result.append([next(i) for i in iterObjs])
    except StopIteration:
        for i in listOfLists:
            print(len(i))
        raise
    return result


class DataCleaning:
    def __init__(self, year: int, nrows: int = None):
        if year not in [2018, 2019, 2020]:
            raise ValueError(f'wrong year: input was {str(year)}')
        self.trackingFileName = f'tracking{str(year)}.csv'
        self.nrows = nrows
        self.data = None
        self.csvData = None

        self.plays = None

    def getUniquePlay(self, new=False):
        if new:
            print('fetching plays info...')
            playsData = loadData('plays.csv')
            result = 'Return'
            playtype = ['Punt', 'Kickoff']
            plays = []
            for row in playsData.itertuples(name=None):
                if row[9] == result and row[8] in playtype:
                    # punt = 0, kickoff = 1
                    returnerID = None
                    try:
                        returnerID = int(row[11])
                    except ValueError as err:
                        continue
                    plays.append([uniquePlayID(row[1], row[2]), [returnerID, row[8] == 'Kickoff']])
            json.dump(plays, open(uniquePlayFileName, 'w'))
            print('finished fetching plays info')
        playsData = json.load(open(uniquePlayFileName, 'r'))
        self.plays = {}
        for uid, play in playsData:
            self.plays[int(uid)] = play

    def dataDownsizing(self) -> []:
        if self.plays is None:
            self.getUniquePlay()
        print('downsizing data...')
        rawData = loadData(self.trackingFileName)
        print('finished loading tracking csv file')

        t0 = time()
        # data = [[gamePlayID, returnerIndex, type, playerlist, playData)]]
        # numpyData = [gameDataAtEachTimeFrame]
        # gameDataAtEachTimeFrame = [timeFromStart, *ballData, *homeRunPlayerData, *awayPlayerData]
        # homeRunPlayerData = [*playerData]  # awayPlayerData is similar
        data = []
        rowIter = rawData.itertuples(name=None)
        newRow = None
        lastRow = None
        # needed data: 1: time, 2: x, 3: y, 4: v, 5: a, 6: d, 7: ori, 8: dir, 9: event, 10: playerID, 12: jersyNum,
        #              14: team, 15: frame, 16: gameID, 17: playID
        while True:
            try:
                newRow = next(rowIter)
            except StopIteration:
                break
            playDataFull = None
            playerList = None
            playData = None
            playID = uniquePlayID(newRow[16], newRow[17])
            process = playID in self.plays
            n = None
            if process:
                # gathering data: reternerID is in place of returnerIndex,
                # players not in correct order,
                # playerList currently holds data = [(playerID, team, jerseyNum)]

                playDataFull = [playID, *self.plays[playID], [], []]
                playerList = playDataFull[3]
                playerList.append(getPlayerInfo(newRow))
                playData = playDataFull[4]
                playerData = []
                headerData = []

                while True:
                    headerData.append(newRow[9])
                    playerData.append(getPlayerData(newRow))

                    del (lastRow)
                    lastRow = newRow
                    newRow = next(rowIter)
                    if lastRow is None or lastRow[10] != newRow[10]:
                        n = lastRow[15]
                        playData.append(playerData)
                        break
                for _ in range(21):
                    playerList.append(getPlayerInfo(newRow))
                    playerData = []
                    for _ in range(n):
                        playerData.append(getPlayerData(newRow))
                        del (newRow)
                        newRow = next(rowIter)
                    playData.append(playerData)
                playerData = []
                for _ in range(n - 1):
                    playerData.append(getBallData(newRow))
                    del (newRow)
                    newRow = next(rowIter)
                playerData.append(getBallData(newRow))
                playData.append(playerData)
                del (newRow)
                # now: playData = [headerData, *players, ball]

                # analyzing numpyData
                homeTeamPlayer = []
                awayTeamPlayer = []
                homeTeam = []
                awayTeam = []
                for i in range(22):
                    player = playerList[i]
                    if player[1]:
                        homeTeamPlayer.append((player[0], player[2]))
                        homeTeam += transpose(playData[i])
                    else:
                        awayTeamPlayer.append((player[0], player[2]))
                        awayTeam += transpose(playData[i])
                playerList = homeTeamPlayer + awayTeamPlayer
                for i in range(22):
                    if playDataFull[1] == playerList[i][0]:
                        playDataFull[1] = i
                newPlayData = [headerData, *transpose(playData[22]), *homeTeam, *awayTeam]
                playDataFull[3] = playerList
                playDataFull[4] = newPlayData
                data.append(playDataFull)
            else:
                while True:
                    del (lastRow)
                    lastRow = newRow
                    newRow = next(rowIter)

                    if lastRow is None or lastRow[10] != newRow[10]:
                        n = lastRow[15]
                        break
                for _ in range(22 * n - 1):
                    next(rowIter)

        print(f'finished downsizing data, took {time() - t0} seconds')
        return data

    def restructure(self, data):
        print('restructuring downsized data...')
        self.data = [i[:4] for i in data]
        csvData = []
        csvDataList = [transpose(i[4]) for i in data]
        # ncols = len(csvDataList[0][0])
        rowPos = 0
        for i in range(len(self.data)):
            playData = csvDataList[i]
            nrows = len(playData)
            csvData += playData
            self.data[i].append((rowPos, nrows))
            rowPos += nrows
        self.csvData = pd.DataFrame(csvData)
        print('finished restructuring data')

    def save(self, playInfoFileName: str, playDataFileName: str):
        print('saving data to files...')
        if self.data is None:
            raise ValueError("data is empty")
        json.dump(self.data, open(playInfoFileName, 'w'))
        if not isinstance(self.csvData, pd.DataFrame):
            raise ValueError(f"csvData is not DataFrame, but of type {type(self.csvData)}")
        self.csvData.to_csv(playDataFileName, mode='w', index=False, header=False)
        print('finished saving data to files')


    def load(self, playInfoFileName: str, playDataFileName: str):
        print('loading data from files...')
        self.data = json.load(open(playInfoFileName, 'r'))
        self.csvData = pd.read_csv(playDataFileName)
        print('finished loading data')

    def saveToCSV(self, filename: str, data):
        print('saving data to csv file...')
        playCols = ['gamePlayID', 'returnerIndex', 'type', 'event']
        dataCols = ['x', 'y', 'v', 'a', 'distance', 'orientation', 'direction']
        ballCols = ['ball ' + i for i in dataCols[:5]]
        playerCols = ['playerID', 'jerseyNum'] + dataCols
        playerCols = [[f'#{i} ' + j for j in playerCols] for i in range(22)]
        cols = playCols + ballCols + [j for i in playerCols for j in i]

        pd.DataFrame(columns=cols).to_csv(filename, mode='w', index=False)
        for play in tqdm(data):
            n = len(play[4][0])
            base = pd.DataFrame(index=range(n))
            # other data
            base[playCols[0]] = play[0]
            base[playCols[1]] = play[1]
            base[playCols[2]] = 'Kickoff' if play[2] else 'Punt'
            # event
            base[playCols[3]] = play[4][0]
            # ball
            for i in range(len(ballCols)):
                base[ballCols[i]] = play[4][i + 1]
            # players
            for i in range(22):
                base[cols[9 + i * 9]] = play[3][i][0]
                base[cols[10 + i * 9]] = play[3][i][1]
                for j in range(len(dataCols)):
                    base[cols[11 + j + i * 9]] = play[4][6 + j + i * 7]

            base.to_csv(filename, mode='a', header=False, index=False)
        print('finished')

    def testingProcesses(self):
        events = set()
        for i in tqdm(self.csvData.itertuples(name=None)):
            events.add(i[1])
        print(events)
        print([str(type(i)) for i in events])


if __name__ == '__main__':
    playInfoFileName = 'DownsizedData/playInfo2018.json'
    playDataFileName = 'DownsizedData/playData2018.csv'
    csvFileName = 'DownsizedData/combinedData2018.csv'

    data = DataCleaning(2018, nrows=10)

    # data.getUniquePlay(new=True)
    # playInfoData = data.dataDownsizing()
    # data.restructure(playInfoData)
    # data.save(playInfoFileName, playDataFileName)
    # data.saveToCSV(csvFileName, playInfoData)

    data.load(playInfoFileName, playDataFileName)
    data.testingProcesses()




