import pandas as pd
#
# sampleData = []
# with open('rawData/tracking2018.csv', 'r') as file:
#     dataIter = csv.reader(file)
#     next(dataIter)
#     for i in range(1):
#         sampleData.append(next(dataIter))
# # print(sampleData)

playCols = ['gamePlayID', 'returnerIndex', 'type', 'event']
dataCols = ['x', 'y', 'v', 'a', 'distance', 'orientation', 'direction']
ballCols = ['ball ' + i for i in dataCols[:5]]
playerCols = ['playerID', 'jerseyNum'] + dataCols
playerCols = [[f'#{i} ' + j for j in playerCols] for i in range(22)]
cols = playCols + ballCols + [j for i in playerCols for j in i]

