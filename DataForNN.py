from copy import copy

import numpy as np
import pandas as pd
from time import time


from DownsizedData import DownsizedData
from PlaysAnalysis import uniquePlayID
from TacklePlayInfo import TacklePlayInfo
from ScountingAnalysis import ScountingAnalysis

distanceStartIdx = 160
tackleAttemptDistance = 1.5


def distanceJIT(data, returnerPos):
    n = data.shape[0]
    result = np.empty((n, 22))
    for i in np.arange(22):
        result[:, i] = np.sqrt(
            (returnerPos[:, 0] - data[:, 6 + 7 * i]) ** 2 + (returnerPos[:, 1] - data[:, 7 + 7 * i]) ** 2)
    return result



class DataForNN:
    def __init__(self):
        self.frameInfos = None
        self.csvData = None

    def getData(self, events: [int]):
        dataList = []
        for event in events:
            downsizedDataFileNames = [f'DownsizedData/playInfo_event_{event}.json',
                                      f'DownsizedData/playData_event_{event}.csv']
            dataList.append(DownsizedData.fromSave(*downsizedDataFileNames))
        data = DownsizedData.combine(dataList)
        return data

    def addTackler(self, data: DownsizedData):
        scountingData = ScountingAnalysis()
        playIDList = [playInfo.playID for playInfo in data.playInfos]
        tacklerInfo = scountingData.tacklerInfo(playIDList)
        for playInfo in data.playInfos:
            tacklers = tacklerInfo[playInfo.playID]
            playerList = playInfo.playerList
            tacklerIdxs = []
            for tackler in tacklers:
                tacklerIdx = 0
                for player in playerList:
                    if player == tackler[0]:
                        break
                    tacklerIdx += 1
                tacklerIdxs.append((tacklerIdx, tackler[1]))
            playInfo.tacklerIdx = tacklerIdxs
        return data

    def addDistanceData(self, data):
        npData = np.asarray(data.playData, dtype=float)
        returnerPos = []
        for playInfo in data.playInfos:
            dataIndexes = playInfo.dataIndexes
            i = playInfo.returnerIdx
            returnerPos.append(npData[dataIndexes[0]:dataIndexes[1], 6 + 7 * i:8 + 7 * i])
        returnerPos = np.vstack(returnerPos)
        distanceData = distanceJIT(npData, returnerPos)
        npData = np.hstack([npData, distanceData])
        data.playData = npData
        return data

    def framesToCSVForSpace(self, saveFileName=None):
        data = self.csvData
        frameList = []
        for playInfo in self.frameInfos:
            # player list reorder
            returnerIdx = playInfo.returnerIdx
            ri = (0, returnerIdx, 11) if returnerIdx < 11 else (11, returnerIdx, 22)
            ti = (0, 11) if returnerIdx >= 11 else (11, 22)
            pl = playInfo.playerList
            newPlayerList = [*pl[ri[1]:ri[2]], *pl[ri[0]:ri[1]], *pl[ti[0]:ti[1]]]

            # frame data reorder
            fi = playInfo.dataIndexes
            returnerDataIdx = 6 + 7 * returnerIdx
            returnerTeamIdx = 6 if returnerIdx < 11 else 83
            ri = (returnerTeamIdx, returnerDataIdx, returnerTeamIdx + 77)
            ti = (6, 83) if returnerIdx >= 11 else (83, 160)
            d = data
            frameData = [d[fi, ri[1]:ri[2]], d[fi, ri[0]:ri[1]], d[fi, ti[0]:ti[1]]]
            frameData = np.concatenate(frameData)
            frameData = frameData.tolist()
            frameCSV = [playInfo.playID, playInfo.playType, *newPlayerList, *frameData]
            frameList.append(frameCSV)
        if saveFileName is not None:
            pd.DataFrame(frameList).to_csv(saveFileName)
        return frameList

    def framesToCSVForNN(self, saveFileName=None):
        data = self.csvData
        frameList = []
        for playInfo in self.frameInfos:
            playID = playInfo.playID
            playType = playInfo.playType
            returnerID = playInfo.getReturnerID()
            tacklerID = playInfo.getTacklerID()
            success = playInfo.getSuccess()
            ri = (6 + 7 * playInfo.returnerIdx, 13 + 7 * playInfo.returnerIdx)
            ti = (6 + 7 * playInfo.tacklerIdx[0], 13 + 7 * playInfo.tacklerIdx[0])
            fi = playInfo.dataIndexes
            d = data
            frameData = [d[fi, ri[0]:ri[1]], d[fi, ti[0]:ti[1]]]
            frameData = np.concatenate(frameData).tolist()
            frameCSV = [playID, playType, returnerID, tacklerID, *frameData, success]
            frameList.append(frameCSV)
        if saveFileName is not None:
            pd.DataFrame(frameList).to_csv(saveFileName)
        return frameList

    def getKeyFrames(self, data: DownsizedData):
        # get the first frame when the trackler get within 1.5 yard radius of the returner

        #
        if not isinstance(data.playData, np.ndarray):
            raise TypeError(
                f'DataForNN.getKeyFrames() only takes data whose playData is in ndarray, not {type(data.playData)}')
        frames = []
        for playInfo in data.playInfos:
            dataIndexes = playInfo.dataIndexes
            # returnerIdx = play[1]
            for tackler in playInfo.tacklerIdx:
                tacklerIdx = tackler[0]
                for frameIdx in range(*dataIndexes):
                    distance = data.playData[frameIdx, distanceStartIdx + tacklerIdx]
                    if distance < tackleAttemptDistance:
                        newPlayInfo = copy(playInfo)
                        newPlayInfo.tacklerIdx = tackler
                        newPlayInfo.dataIndexes = frameIdx
                        frames.append(newPlayInfo)
                        break
        self.frameInfos = frames
        self.csvData = data.playData
        return [frames, data.playData]

    def getTacklerFrames(self, data: DownsizedData):
        frames = []
        csvData = copy(data.playData)
        for playInfo in data.playInfos:
            returnerIdx = playInfo.returnerIdx
            playerList = playInfo.playerList
            for playerIdx in range(22):
                if playerIdx == returnerIdx:
                    continue
                dataIndexes = playInfo.dataIndexes
                tackleFrameIdx = None
                closeContact = False
                for frameIdx in range(dataIndexes):
                    distance = data.playData[frameIdx, distanceStartIdx + playerIdx]
                    if distance < tackleAttemptDistance:
                        if not closeContact:
                            tackleFrameIdx = frameIdx
                            closeContact = True
                    else:
                        closeContact = False
                if tackleFrameIdx is not None:
                    newPlayInfo = copy(playInfo)
                    newPlayInfo.tacklerIdx = playerIdx
                    newPlayInfo.dataIndexes = tackleFrameIdx
                    frames.append(newPlayInfo)
        self.frameinfos = frames
        self.csvData = data.playData
        return [frames, data.playData]






    @staticmethod
    def prepareData():
        processor = DataForNN()
        data = processor.getData([3, 5])
        data = processor.addTackler(data)
        data = processor.addDistanceData(data)
        spaceValueFileName = 'AnalyzedData/spaceValueSource.csv'
        nnDataFileName = 'AnalyzedData/nnDataSource.csv'
        processor.getKeyFrames(data)
        processor.framesToCSVForSpace(saveFileName=spaceValueFileName)
        processor.framesToCSVForNN(saveFileName=nnDataFileName)


if __name__ == '__main__':
    DataForNN.prepareData()
