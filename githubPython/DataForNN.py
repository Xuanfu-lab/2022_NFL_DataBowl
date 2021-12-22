import numpy as np
import pandas as pd
from numba import jit
from time import time

from DownsizedData import DownsizedData
from PlaysAnalysis import uniquePlayID
from ScountingAnalysis import ScountingAnalysis


# @jit(parallel=True)
def distanceJIT(data, returnerPos):
    n = data.shape[0]
    result = np.empty((n, 22))
    for i in np.arange(22):
        result[:, i] = np.sqrt(
            (returnerPos[:, 0] - data[:, 6 + 7 * i]) ** 2 + (returnerPos[:, 1] - data[:, 7 + 7 * i]) ** 2)
    return result


class DataForNN:
    def __init__(self):
        pass

    def getData(self, events: [int]):
        dataList = []
        for event in events:
            downsizedDataFileNames = [f'DownsizedData/playInfo_event_{event}.json',
                                      f'DownsizedData/playData_event_{event}.csv']
            dataList.append(DownsizedData.fromSave(*downsizedDataFileNames))
        data = DownsizedData.combine(dataList)
        return data

    def addDistanceData(self, data):
        npData = np.asarray(data.playData, dtype=float)
        returnerPos = []
        for play in data.playInfo:
            rows = play[4]
            i = play[1]
            returnerPos.append(npData[rows[0]:rows[1], 6 + 7 * i:8 + 7 * i])
        returnerPos = np.vstack(returnerPos)
        distanceData = distanceJIT(npData, returnerPos)
        npData = np.hstack([npData, distanceData])
        data.playData = npData
        return data

    def addTackler(self, data: DownsizedData):
        scountingData = ScountingAnalysis()
        playIDList = [play[0] for play in data.playInfo]
        tacklerInfo = scountingData.tacklerInfo(playIDList)
        for play in data.playInfo:
            tacklers = tacklerInfo[play[0]]
            playerList = play[3]
            tacklerIdxs = []
            for tackler in tacklers:
                tacklerIdx = 0
                for player in playerList:
                    if player[0] == tackler[0]:
                        break
                    tacklerIdx += 1
                tacklerIdxs.append((tacklerIdx, tackler[1]))
            play.append(tacklerIdxs)
        return data


    def getKeyFrame(self, data):
        # get the first frame when the trackler get within 1.5 yard radius of the returner

        #
        frames = []
        for play in data.playInfo:
            break
            for tackler in play[5]:
                break



    def finalProcess0(self):
        # for space score calculation
        # -- includes only one frame for each tackler for each play
        # -- all frames needs data for each player



        pass


    def finalProcess1(self):
        # for nn version 1
        # data = [[returner x, y, ..., tackler x, y, ..., space, success]]

        pass


if __name__ == '__main__':
    test = DataForNN()
    t0 = time()
    data = test.getData([3, 5])

    print('preparation time:', time() - t0)
    t0 = time()
    data = test.addTackler(data)
    data = test.addDistanceData(data)
    print('processing time:', time() - t0)
