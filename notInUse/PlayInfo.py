from PlaysAnalysis import PlaysAnalysis, uniquePlayID


class PlayInfo:
    plays = None

    @staticmethod
    def getPlays(plays=None):
        if plays is None:
            PlayInfo.plays = PlaysAnalysis().getUniquePlay()
        else:
            PlayInfo.plays = plays

    def __init__(self,
                 playID,
                 playType=None,
                 playerList=None,
                 dataIndexes=None):
        self.playID = playID
        self.playType = playType
        self.playerList = playerList
        self.dataIndexes = dataIndexes




    def toJSON(self):
        return [self.playID,
                self.dataIndexes,
                self.playType,
                self.playerList]

    @classmethod
    def fromJSON(cls, playInfo):
        playID, dataIndexes, playType, playerList = playInfo
        return cls(playID,
                   dataIndexes=dataIndexes,
                   playType=playType,
                   playerList=playerList)

    @classmethod
    def __copy__(self, playInfo):
        newObj = PlayInfo(playInfo)


    @classmethod
    def fromGameID(cls, gameID, playID):
        return cls(uniquePlayID(gameID, playID))
