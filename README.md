# 2022_NFL_DataBowl

| Name of Collaborator | e-mail | Role | School & Major |
| ------------- | ------------- | ------------- | ------------- |
| Hongze Liu    | honzliu@gmail.com  | Project Manager, Visualization | UC Berkeley: Mathematics, Statistics, History (class of 2020)  |
| Qitai Meng    | neomeng@berkeley.edu   | Python Engineer, High Performance Computing  | UC Berkeley: Mechanical Engineering (class of 2022)  |
| Xuanfu Lu     | xuanfu724@gmail.com  | Python Engineer, Neural Network & Machine Learning | UC Berkeley: Statistics, Economics (class of 2020) |

Report File is decompose-tackling-a-neural-network-approach.ipynb
Alternatively https://www.kaggle.com/hongzeliu7/decompose-tackling-a-neural-network-approach#Decompose-Tackling,-a-Neural-Network-Approach

Steps to reproduce results:

1. Download all files from this repository
2. Install necessary packages, and set working directory to the downloaded path
3. Download raw data from https://www.kaggle.com/c/nfl-big-data-bowl-2022/data
4. Store raw data in */rawData*
5. Run *XXXX.py*
6. Run *XXXX.py*
7. After running the above data prep & cleaning steps, folder *AnalyzedData/* should have *nnDataSource.csv, spaceValues.csv, spaceValueSource.csv*
8. *AnalyzedData/game1raw.csv* was manually created using Excel from *DownsizedData/combinedData2018.csv* (row 505-597, and columns are rearranged)
9. Run *game1.Rmd*, you will get *AnalyzedData/game1.csv*
10. Run *ExpandedData.Rmd*, you will get *AnalyzedData/big.csv* and *AnalyzedData/biggg.csv*
11. Run *NNModel-AllPlayers.ipynb* in Jupyter Notebook, you will get the neural network model and its results. Additionally it will write out 2 csv: *AnalyzedData/returnerScoreBoard.csv* and *AnalyzedData/tacklerScoreBoard.csv*, which were used in our final report.
12. Run ProduceTable.Rmd to reproduce graphs used in the report
