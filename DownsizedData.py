import pandas as pd
from time import time, sleep
from tqdm import tqdm
import json
from threading import Thread

from PlaysAnalysis import PlaysAnalysis, uniquePlayID
from TacklePlayInfo import TacklePlayInfo

uniquePlayFileName = 'DownsizedData/uniquePlays.json'
nan = float('nan')


# def loadData(rawFilename: str, nrows: int = None) -> pd.DataFrame:
#     filename = 'rawData/' + rawFilename
#     if nrows is None:
#         return pd.read_csv(filename)
#     else:
#         return pd.read_csv(filename, nrows=nrows)


def getPlayerInfo(row):
    return (int(row[10]), row[14] == 'home')


def getPlayerData(row):
    return [row[2], row[3], row[4], row[5], row[6], row[7], row[8]]


def getBallData(row):
    return [row[2], row[3], row[4], row[5], row[6]]


# puntEventList = ['ball_snap', 'punt', 'punt_received']
puntEventDict = {'ball_snap': 1, 'punt': 2, 'punt_received': 3}


def puntEvent(event: str) -> int:
    return puntEventDict.get(event, 0)


# kickoffEventList = ['kickoff', 'kick_received']
kickoffEventDict = {'kickoff': 4, 'kick_received': 5}


def kickoffEvent(event: str) -> int:
    return kickoffEventDict.get(event, 0)


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


class DownsizedData:
    def __init__(self, fileName, data=None, csvData=None):

        self.rawDataFileName = fileName
        self.playInfos = data
        self.playData = csvData
        self.plays = PlaysAnalysis().getUniquePlay()
        TacklePlayInfo.getPlays(self.plays)

    def dataDownsizing(self) -> []:

        print('downsizing data...')
        rawData = pd.read_csv(self.rawDataFileName)
        print('finished loading tracking csv file')

        t0 = time()
        # data = [[playInfoObj, playData]]
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
            playID = uniquePlayID(newRow[16], newRow[17])
            process = playID in self.plays
            n = None
            if process:
                # gathering data: reternerID is in place of returnerIndex,
                # players not in correct order,
                # playerList currently holds data = [(playerID, team, jerseyNum)]

                playData = []
                playerList = [getPlayerInfo(newRow)]
                playInfo = TacklePlayInfo(playID, playerList=playerList)
                playInfo.getInfoFromPlays()
                # playDataFull = [playInfo, playData]

                # playDataFull = [[playID, *self.plays[playID], []], []]
                # playType = playDataFull[0][2]
                # playerList = playDataFull[0][3]
                # playerList.append(getPlayerInfo(newRow))
                # playData = playDataFull[1]
                playerData = []
                headerData = []
                event = 0

                while True:
                    eventStr = newRow[9]
                    eventNum = puntEvent(eventStr) if playInfo.playType == 0 else kickoffEvent(eventStr)
                    if eventNum != 0:
                        event = eventNum
                    headerData.append(event)
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
                    if player[1] == 1:
                        homeTeamPlayer.append(player[0])
                        homeTeam += transpose(playData[i])
                    else:
                        awayTeamPlayer.append(player[0])
                        awayTeam += transpose(playData[i])
                playerList = homeTeamPlayer + awayTeamPlayer
                for i in range(22):
                    if playInfo.returnerID == playerList[i]:
                        playInfo.returnerIdx = i
                newPlayData = [headerData, *transpose(playData[22]), *homeTeam, *awayTeam]
                playInfo.playerList = playerList
                data.append([playInfo, newPlayData])
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

    def restructure(self, data, transposeCSV=False):
        # csv = [[header * 1, ball * 5, home * 11 * 7, away * 11 * 7]]
        print('restructuring downsized data...')
        self.playInfos = []
        self.playData = []
        rowPos = 0
        for playInfo, playData in data:
            if transposeCSV:
                playData = transpose(playData)
            nrows = len(playData)
            playInfo.dataIndexes = (rowPos, rowPos + nrows)
            self.playInfos.append(playInfo)
            self.playData += playData
            rowPos += nrows

        print('finished restructuring data')

    def save(self, playInfoFileName: str, playDataFileName: str):
        print('saving data to files...')
        if self.playInfos is None:
            raise ValueError("data is empty")
        json.dump([playInfo.toJSON() for playInfo in self.playInfos], open(playInfoFileName, 'w'))
        if self.playData is None:
            raise ValueError(f"csvData is empty")
        pd.DataFrame(self.playData).to_csv(playDataFileName, mode='w', index=False, header=False)
        print('finished saving data to files')

    def load(self, playInfoFileName: str, playDataFileName: str, dataFrame=False):
        print('loading data from files...')
        self.playInfos = [TacklePlayInfo.fromJSON(playInfo) for playInfo in json.load(open(playInfoFileName, 'r'))]
        csvData = pd.read_csv(playDataFileName, header=None)
        if dataFrame:
            print('finished loading data')
            self.playData = csvData
            return self.playInfos, csvData
        else:
            self.playData = csvData.values.tolist()
            print('finished loading data')
            return self.playInfos, self.playData

    @classmethod
    def fromSave(cls, playInfoFileName: str, playDataFileName: str, dataFrame=False):
        data = cls()
        data.load(playInfoFileName, playDataFileName, dataFrame)
        return data

    @classmethod
    def combine(cls, objs):
        print('start combining...')
        playInfoList = objs[0].playInfos
        playData = objs[0].playData
        n = 0
        for i in range(len(objs) - 1):
            n += len(objs[i].playData)
            playInfoListTemp = objs[i + 1].playInfos
            for playInfo in playInfoListTemp:
                oldIndexes = playInfo.dataIndexes
                playInfo.dataIndexes = (oldIndexes[0] + n, oldIndexes[1] + n)
            playInfoList += playInfoListTemp
            playData += objs[i + 1].playData
        print('finished combining')
        return cls(data=playInfoList, csvData=playData)

    # seperate punt and kickoff, and their events, probably only for testing
    def seperate0(self, save=False, year=''):
        print('seperating data according to both punt and kickoff...')
        nObjs = 5
        fileNames = [[f'DownsizedData/playInfo_event_{i + 1}.json',
                      f'DownsizedData/playData_event_{i + 1}.csv'] for i in range(nObjs)]

        # [eventType: [play: [playInfo, playData]]]
        dataList = [[] for _ in range(nObjs)]
        eventDataLocal = None
        for playInfo in self.playInfos:
            index = playInfo.dataIndexes
            event = 0
            try:
                for i in range(*index):
                    frame = self.playData[i]
                    newEvent = int(frame[0])
                    if newEvent == 0:
                        continue
                    eventType = dataList[newEvent - 1]
                    if newEvent != event:
                        event = newEvent
                        eventDataLocal = []
                        eventType.append([playInfo, eventDataLocal])
                    eventDataLocal.append(frame)
            except IndexError:
                print(len(self.playData), self.playInfos[-1][4])
                raise
        print('saving files...')
        objList = []
        for i in range(nObjs):
            eventType = dataList[i]
            eventData = DownsizedData(self.year)
            eventData.restructure(eventType)
            eventData.save(*fileNames[i])
            objList.append(eventData)
        print('finished seperating files')
        return objList

    def saveToCSV(self, filename: str, data):
        print('saving data to csv file...')
        playCols = ['gamePlayID', 'returnerIndex', 'type', 'event']
        dataCols = ['x', 'y', 'v', 'a', 'distance', 'orientation', 'direction']
        ballCols = ['ball ' + i for i in dataCols[:5]]
        playerCols = ['playerID'] + dataCols
        playerCols = [[f'#{i} ' + j for j in playerCols] for i in range(22)]
        cols = playCols + ballCols + [j for i in playerCols for j in i]
        pd.DataFrame(columns=cols).to_csv(filename, mode='w', index=False)
        for playInfo, playData in tqdm(data):
            n = len(playData[0])
            base = pd.DataFrame(index=range(n))
            # other data
            base[playCols[0]] = playInfo.playID
            base[playCols[1]] = playInfo.returnerIdx
            base[playCols[2]] = 'Kickoff' if playInfo.playType else 'Punt'
            # event
            base[playCols[3]] = playData[0]
            # ball
            for i in range(len(ballCols)):
                base[ballCols[i]] = playData[i + 1]
            # players
            for i in range(22):
                base[cols[9 + i * 8]] = playInfo.playerList[i]
                for j in range(len(dataCols)):
                    base[cols[10 + j + i * 8]] = playData[6 + j + i * 7]
            base.to_csv(filename, mode='a', header=False, index=False)
        print('finished')

    @staticmethod
    def initialize(fileNames, fromRawData=True):
        data = None
        if fromRawData:
            dataList = []
            for trackingDataFileName in fileNames['tracking']:
                data = DownsizedData(trackingDataFileName)
                playInfoData = data.dataDownsizing()
                data.restructure(playInfoData, transposeCSV=True)
                dataList.append(data)
            data = DownsizedData.combine(dataList)
            data.save('DownsizedData/playInfo.json', 'DownsizedData/playData.csv')
        else:
            data = DownsizedData()
            data.load('DownsizedData/playInfo.json', 'DownsizedData/playData.csv')
        data.seperate0(save=True)


if __name__ == '__main__':
    years = [2018, 2019, 2020]
    dataList = []
    for year in years:
        playInfoFileName = f'DownsizedData/playInfo{year}.json'
        playDataFileName = f'DownsizedData/playData{year}.csv'
        csvFileName = f'DownsizedData/combinedData{year}.csv'

        data = DownsizedData(year)
        playInfoData = data.dataDownsizing()
        data.restructure(playInfoData, transposeCSV=True)
        data.save(playInfoFileName, playDataFileName)

        # data.load(playInfoFileName, playDataFileName)
        dataList.append(data)
    data = DownsizedData.combine(dataList)
    data.save('DownsizedData/playInfo.json', 'DownsizedData/playData.csv')
    data.saveToCSV(csvFileName, playInfoData)
    data.seperate0(save=True)

    # data.getUniquePlay(new=True)
    # playInfoData = data.dataDownsizing()
    # data.restructure(playInfoData, transposeCSV=True)
    # data.save(playInfoFileName, playDataFileName)
    # # data.load(playInfoFileName, playDataFileName)
    # data.seperate0(save=True)
    # data.saveToCSV(csvFileName, playInfoData)

    # data.load(playInfoFileName, playDataFileName)
    # data.testingProcesses()
