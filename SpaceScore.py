import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

from scipy.spatial.distance import euclidean
from tqdm import tqdm

nSample = 100
boundingSquareEdgeL = 10


def radius_calc(dist_to_ball):
    return 4 + 6 * (dist_to_ball >= 15) + (dist_to_ball ** 3) / 560 * (dist_to_ball < 15)


def compute_influence(x_point, y_point, x0, y0, x, y, s, o):
    # x, y, s, a, dis, o, dire
    '''Compute the influence of a certain player over a coordinate (x, y) of the pitch
    '''
    point = np.asarray([x_point, y_point])
    theta = math.radians(o)
    player_coords = np.asarray([x, y])
    ball_coords = np.asarray([x0, y0])
    dist_to_ball = euclidean(player_coords, ball_coords)

    S_ratio = (s / 13) ** 2  # we set max_speed to 13 m/s
    RADIUS = radius_calc(dist_to_ball)

    S_matrix = np.matrix([[RADIUS * (1 + S_ratio), 0], [0, RADIUS * (1 - S_ratio)]])
    R_matrix = np.matrix([[np.cos(theta), - np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    COV_matrix = np.dot(np.dot(np.dot(R_matrix, S_matrix), S_matrix), np.linalg.inv(R_matrix))

    norm_fact = (1 / 2 * np.pi) * (1 / np.sqrt(np.linalg.det(COV_matrix)))
    mu_play = player_coords + s * np.array([np.cos(theta), np.sin(theta)]) / 2

    intermed_scalar_player = np.dot(np.dot((player_coords - mu_play),
                                           np.linalg.inv(COV_matrix)),
                                    np.transpose((player_coords - mu_play)))
    player_influence = norm_fact * np.exp(- 0.5 * intermed_scalar_player[0, 0])

    intermed_scalar_point = np.dot(np.dot((point - mu_play),
                                          np.linalg.inv(COV_matrix)),
                                   np.transpose((point - mu_play)))
    point_influence = norm_fact * np.exp(- 0.5 * intermed_scalar_point[0, 0])

    return point_influence / player_influence


def pitch_control(dataFileName, spaceScoreFileName):
    idx = range(24, 178)
    idx = [str(i) for i in idx]
    data = pd.read_csv(dataFileName, header=0, index_col=0)[idx].to_numpy()
    scoreVec = []
    scoreVec = []
    for row in tqdm(data):
        xr, yr = row[:2]
        score = 0
        for i in range(11):
            basei = 7 * i
            x, y, v = row[basei:basei + 3]
            o = row[basei + 5]
            score += compute_influence(xr, yr, xr, yr, x, y, v, o)
            basei = 77 + 7 * i
            x, y, v = row[basei:basei + 3]
            o = row[basei + 5]
            score -= compute_influence(xr, yr, xr, yr, x, y, v, o)
        scoreVec.append(score)
    result = pd.DataFrame()
    result['pitch control'] = scoreVec
    result.to_csv(spaceScoreFileName)
    return scoreVec


def computeTackleAblt(rx, ry, rv, rdir, tx, ty, tv, tdir):
    centerPointx = (tx - rx) / 2 + rx
    centerPointy = (ty - ry) / 2 + ry
    xSamplePoints = np.linspace(centerPointx - boundingSquareEdgeL / 2, centerPointx + boundingSquareEdgeL / 2, nSample)
    ySamplePoints = np.linspace(centerPointy - boundingSquareEdgeL / 2, centerPointy + boundingSquareEdgeL / 2, nSample)
    totalScore = 0
    scoreMap = []
    for ys in ySamplePoints:
        scoreList = []
        for xs in xSamplePoints:
            rscore = compute_influence(xs, ys, rx, ry, rx, ry, rv, rdir)
            tscore = compute_influence(xs, ys, rx, ry, tx, ty, tv, tdir)
            score = rscore * tscore
            scoreList.append((score, rscore, tscore))
            totalScore += score
        scoreMap.append(scoreList)

    return score, scoreMap, xSamplePoints, ySamplePoints


if __name__ == '__main__':

    # visualization code:
    score, scoreMap, x, y = computeTackleAblt(10, 10, 10, 45,
                                              10, 12, 10, 90)
    print(score)

    X, Y = np.meshgrid(x, y)
    score = np.flip(np.asarray([[i[0] for i in j] for j in scoreMap]), axis=0)
    scoreR = np.flip(np.asarray([[i[1] for i in j] for j in scoreMap]), axis=0)
    scoreT = np.flip(np.asarray([[i[2] for i in j] for j in scoreMap]), axis=0)

    fig = plt.figure()
    plot0 = fig.add_subplot(131, projection='3d')
    plot1 = fig.add_subplot(132, projection='3d')
    plot2 = fig.add_subplot(133, projection='3d')

    plot0.plot_surface(X, Y, score, cmap=cm.coolwarm)
    plot1.plot_surface(X, Y, scoreR, cmap=cm.coolwarm)
    plot2.plot_surface(X, Y, scoreT, cmap=cm.coolwarm)

    plot0.set_xlabel('x')
    plot0.set_ylabel('y')
    plot1.set_xlabel('x')
    plot1.set_ylabel('y')
    plot2.set_xlabel('x')
    plot2.set_ylabel('y')
    plot0.set_title("Total Influence")
    plot1.set_title("Returner Influence")
    plot2.set_title("Tackler Influence")
    plt.show()

    # write out csv code
    # pitch_control('AnalyzedData/spaceValueSource.csv', 'AnalyzedData/spaceValues.csv')
