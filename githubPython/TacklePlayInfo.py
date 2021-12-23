from PlayInfo import PlayInfo


class TacklePlayInfo(PlayInfo):

    def __init__(self,
                 playID,
                 returnerIdx=None,
                 tacklerIdx=None,
                 playType=None,
                 playerList=None,
                 dataIndexes=None):
        super().__init__(playID,
                         playType=playType,
                         playerList=playerList,
                         dataIndexes=dataIndexes)
        self.returnerIdx = returnerIdx
        self.tacklerIdx = tacklerIdx

    def getInfoFromPlays(self):
        self.returnerID, self.playType = PlayInfo.plays[self.playID]

    def getReturnerID(self):
        return self.playerList[self.returnerIdx]

    def getTacklerID(self):
        return self.playerList[self.tacklerIdx[0]]

    def getSuccess(self):
        return self.tacklerIdx[1]

    def toJSON(self):
        return super().toJSON() + [self.returnerIdx, self.tacklerIdx]

    @classmethod
    def fromJSON(cls, playInfo):
        playID, dataIndexes, playType, playerList, returnerIdx, tacklerIdx = playInfo
        return cls(playID,
                   dataIndexes=dataIndexes,
                   playType=playType,
                   returnerIdx=returnerIdx,
                   tacklerIdx=tacklerIdx,
                   playerList=playerList)

    @classmethod
    def __copy__(self, playInfo):
        return TacklePlayInfo.fromJSON(playInfo.toJSON())


if __name__ == '__main__':
    a = TacklePlayInfo(100)
    b = a.toJSON()
    print(b)
