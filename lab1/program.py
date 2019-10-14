import os
import sys

# import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filename = './data/txt/data_group1.txt'
data = pd.read_csv(filename, delimiter=r'\s+', names=['year', 'month', 'flux', 'ssnum'])
array = np.array(data)

# plt.plot(data['x'], data['y'])
# plt.plot(array[0][:], array[1][:])
# fyear = data['year'][0]
# print(fyear)
# lyear = data['year'][-1]
# ycount = lyear - fyear

# print(array[0][0], array[-1][0])
# ycount = array[-1][0] - array[0][0]
# print('ycount', ycount)

# pdata = np.zeros(ycount, 2)
# print('data', data)

pdata = []

grouped = data.groupby('year')
print(grouped)
for gi in grouped:
    # pdata.append(np.mean(gi, 2))
    print(gi)
    pdata.append(pd.DataFrame.mean(gi, 2))

print(pdata)
# for name, group in grouped:
#    print name
#    print group

# print(array)
# plt.show()

def main():
    pass

if __name__ == "__main__":
    main()
