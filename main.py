from PlaysAnalysis import PlaysAnalysis
from PlayerAnalysis import PlayerAnalysis
from DownsizedData import DownsizedData
from DataForNN import DataForNN

def initialize(fileNames):
    PlaysAnalysis.initialize(fileNames)
    PlayerAnalysis.initialize(fileNames)
    DownsizedData.initialize(fileNames)
    DataForNN.initialize(fileNames)
    
    
    
#####################################################

# put the corresponding raw data file names below

fileNames = {'plays': 'rawData/plays.csv',
             'players': 'rawData/players.csv',
             'games': 'rawData/games.csv',
             'scouting': 'rawData/PFFScoutingData.csv',
             'tracking': ['rawData/tracking2018.csv',
                          'rawData/tracking2019.csv',
                          'rawData/tracking2020.csv']
             }








if __name__ == '__main__':
    # run initialize() when it's brand new
    initialize(fileNames)
    DataForNN.prepareData()


