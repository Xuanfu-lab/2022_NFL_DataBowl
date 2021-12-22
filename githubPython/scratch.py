import pandas as pd
#
# sampleData = []
# with open('rawData/tracking2018.csv', 'r') as file:
#     dataIter = csv.reader(file)
#     next(dataIter)
#     for i in range(1):
#         sampleData.append(next(dataIter))
# # print(sampleData)
# print(int(True))


def change(a):
    a[0] = 1

b = [7,8,9]
change(b)
print(b)