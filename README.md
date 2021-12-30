# 2022_NFL_DataBowl
Team name: GoBears

| Name of Collaborator | e-mail | Role | School & Major |
| ------------- | ------------- | ------------- | ------------- |
| Hongze Liu    | honzliu@gmail.com  | Project Lead, Visualization | UC Berkeley: Mathematics, Statistics, History (class of 2020)  |
| Qitai Meng    | neomeng@berkeley.edu   | Python Engineer, High Performance Computing  | UC Berkeley: Mechanical Engineering (class of 2022)  |
| Xuanfu Lu     | xuanfu724@gmail.com  | Python Engineer, Neural Network & Machine Learning | UC Berkeley: Statistics, Economics (class of 2020) |

Report File is **_decompose-tackling-a-neural-network-approach.ipynb_**

Alternatively: https://www.kaggle.com/hongzeliu7/decompose-tackling-a-neural-network-approach

Environment: Python 3.8, R 4.0.3

Steps to reproduce results:

1. Download all files from this repository 
2. Install necessary packages, and set directory to the downloaded path
3. Download raw data from https://www.kaggle.com/c/nfl-big-data-bowl-2022/data, and store raw data in **_rawData/_**
4. Run **_PlaysAnalysis.py_**
5. Run **_main.py_** (runtime ~10 min)
6. After running the above data prep & cleaning steps, folder **_AnalyzedData/_** should have **_nnDataSource.csv, spaceValues.csv, spaceValueSource.csv_**
7. **_AnalyzedData/game1raw.csv_** was manually created using Excel from **_DownsizedData/combinedData2018.csv_** (row 505-597, and columns are rearranged)
8. Run **_game1.Rmd_**, you will get **_AnalyzedData/game1.csv_**
9. Run **_ExpandedData.Rmd_**, you will get **_AnalyzedData/big.csv_** and **_AnalyzedData/biggg.csv_**
10. Run **_NNModel-AllPlayers.ipynb_** in Jupyter Notebook, you will get the neural network model and its results. Additionally it will write out 2 csv: **_AnalyzedData/returnerScoreBoard.csv_** and **_AnalyzedData/tacklerScoreBoard.csv_**, which were used in our final report.
11. Run **_ProduceTable.Rmd_** to reproduce graphs used in the report

Note: Please do not run files in IDE. Raw data (~5GB) is too big and it will cause memory issues within IDE.
