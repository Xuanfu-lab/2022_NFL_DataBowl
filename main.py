


from PlaysAnalysis import PlaysAnalysis
from PlayerAnalysis import PlayerAnalysis
from DownsizedData import DownsizedData
from DataForNN import DataForNN

def initialize():
    PlaysAnalysis.initialize()
    PlayerAnalysis.initialize()
    DownsizedData.initialize()








if __name__ == '__main__':
    # run initialize() when it's brand new
    # initialize()
    DataForNN.prepareData()


