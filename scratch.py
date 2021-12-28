import pandas as pd
import numpy as np

# data
rawDataFileName = 'AnalyzedData/nnDataSource.csv'
rawData = pd.read_csv(rawDataFileName, header=0, index_col=0)
# display(rawData)

rawCols = rawData.columns
cols = rawCols[4:]
xCols = cols[:-1]
yCols = ["18"]
usableData = rawData[cols]

relData = pd.DataFrame()

xr = usableData[xCols[0]].to_numpy()
yr = usableData[xCols[1]].to_numpy()
vr = usableData[xCols[2]].to_numpy()
ar = usableData[xCols[3]].to_numpy()
orir = usableData[xCols[5]].to_numpy()
dirr = usableData[xCols[6]].to_numpy()
xt = usableData[xCols[7]].to_numpy()
yt = usableData[xCols[8]].to_numpy()
vt = usableData[xCols[9]].to_numpy()
at = usableData[xCols[10]].to_numpy()
orit = usableData[xCols[12]].to_numpy()
dirt = usableData[xCols[13]].to_numpy()

orir = -np.gradient(orir - 90)
dirr = -np.gradient(dirr - 90)
orit = -np.gradient(orit - 90)
dirt = -np.gradient(dirt - 90)

relData['x0'] = xr
relData['y0'] = yr
relData['x1'] = xt - xr
relData['y1'] = yt - yr
relData['vx0'] = vr * np.cos(dirr)
relData['vy0'] = vr * np.sin(dirr)
relData['vx1'] = vt * np.cos(dirt)
relData['vy1'] = vt * np.sin(dirt)
relData['a0'] = ar
relData['a1'] = at
relData['dir0'] = dirr
relData['dir1'] = dirt
relData['ori0'] = orir
relData['ori0'] = orit

# normalize by column
# dataRange = [(-10, 130, 140), (0, 53.33, 53.33), (0, 14, 14), (0, 7, 7), (0, 1.4, 1.4), (0, 360, 360), (0, 360, 360)]
# for j in range(2):
#     for i in range(7):
#         col = cols[i + j * 7]
#         usableData[col] = (usableData[col] - dataRange[i][0]) / dataRange[i][2]
# display(usableData)


# Randomly selecting training data

# indexes
Ntotal = relData.shape[0]
trainingIndex = np.random.choice(Ntotal, int(Ntotal * 0.90), replace=False)
validationIndex = np.setdiff1d(np.array(range(Ntotal)), trainingIndex)
# data seperation
tSet = relData.iloc[trainingIndex]
vSet = relData.iloc[validationIndex]

# display(tSet)
# display(vSet)
