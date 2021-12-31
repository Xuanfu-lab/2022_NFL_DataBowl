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
4. Run **_main.py_** (runtime ~10 min. recommend to run in command instead of IDE due to raw data file size). This step transforms data structure. Now one row contains all players' information at one frame, instead of 23 rows. It will also sort frames by event type: {1 = before Punt, 2 = Punt ball in the air, 3 = Punt Return, 4 = before Kickoff, 5 = Kickoff Return). After first run, you can comment out row 36 in **_main.py_** to increase running effiency as it will directly pull information from json files in **_DownsizedData/_**.
5. After running the above data prep & cleaning steps, folder **_AnalyzedData/_** should have **_nnDataSource.csv, spaceValueSource.csv_** and 1 json file, and folder **_DownsizedData/_** should have 13 files
6. **_AnalyzedData/game1raw.csv_** was manually created using Excel from **_DownsizedData/playData_event_3.csv_** (row 1-93, and columns are rearranged)
7. Run **_game1.Rmd_**, you will get **_AnalyzedData/game1.csv_**, which is the data for our sample play Baltimore vs. Cleveland (playID = 2502, GameID = 2018123000)
8. Run **_ExpandedData.Rmd_**, you will get the twice-augmented data **_AnalyzedData/biggg.csv_**, which will be the main data used for our neural network models
9. Run **_NNModel-AllPlayers.ipynb_** in Jupyter Notebook, you will get the neural network models and their results. Additionally it will write out 2 csv: **_AnalyzedData/returnerScoreBoard.csv_** and **_AnalyzedData/tacklerScoreBoard.csv_**, which were included in our final report
10. Run **_SpaceScore.py_** to get the space score example graphs in the report
11. Run **_ProduceTable.Rmd_** to reproduce other graphs used in the report

