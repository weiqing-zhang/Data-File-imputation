import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
from datetime import timedelta
now = datetime.now()
print(now)
#import file as myfile
fileList = ['ES1.csv','ES2.csv']
def calcRow(str1, str2):
    t1 = datetime.strptime(str1,'%m/%d/%Y %H:%M')
    t2 = datetime.strptime(str2,'%m/%d/%Y %H:%M')
    row = 0
    while t1 <= t2 :
        t1 = t1+timedelta(minutes = 15)
        row = row +1
    return row

def impute(filename):
    myfile = myfile = pd.read_csv(filename)
    myfile = myfile.drop_duplicates()
    myfile.fillna('null', inplace=True)
    # myfile = pd.concat(myfile, ignore_index=True)
    # get the heading of columns
    heading = myfile.columns.values
    myfile = myfile.reset_index(drop=True)
    mylist = myfile[heading[0]].tolist()
    # mylist is the list of time(values in the first column
    nullIndex = []
    for i in range(len(mylist)):
        if mylist[i] == 'null':
            nullIndex.append(i)
    if len(nullIndex)>0:
        myfile.drop(index=nullIndex[0], inplace=True)

    str1 = myfile[heading[0]][0]
    mytime = myfile[heading[0]].tolist()
    while 'null' in mytime:
        mytime.remove('null')
    str2 = mytime[-1]
    row = calcRow(str1, str2)

    mylist = myfile[heading[0]].tolist()

    # the index of time added
    i = 0
    while i < row:
        if i > 0:
            currentTime = datetime.strptime(mylist[i], '%m/%d/%Y %H:%M')
            lastTime = datetime.strptime(mylist[i - 1], '%m/%d/%Y %H:%M')
            if currentTime == lastTime + timedelta(minutes=15):
                pass
            elif currentTime <= lastTime:
                del mylist[i]
                myfile.drop(i,inplace=True)
                myfile = myfile.reset_index(drop=True)
                i=i-1
            else:
                newTime = lastTime + timedelta(minutes=15)
                newTime = datetime.strftime(newTime, '%m/%d/%Y %H:%M')
                mylist.insert(i, newTime)
                time = i
                newRow = [[mylist[time]] + ['null'] * (len(heading) - 1)]
                first = myfile.iloc[:time, :]
                last = myfile.iloc[time:, :]
                newRow = pd.DataFrame(newRow, columns=heading)
                myfile = pd.concat([first, newRow, last], ignore_index=True)
                i=i-1
        i = i+1
        r, c = myfile.shape

    return myfile



myfile = impute(fileList[0])
heading = myfile.columns.values


for i in range(len(fileList)):
    if i > 0:
        currentFile= impute(fileList[i])
        cHeading = currentFile.columns.values
        myfile.merge(currentFile, left_on=heading[0],right_on=cHeading[0])
        heading= myfile.columns.values

myfile.fillna('null',inplace=True)



sum = []
heading = myfile.columns.values
time = myfile[heading[0]]
for i in range(len(time)):
    total = 0
    ifnull = False
    for j in range(len(heading)):
        if j > 0:
            try:
                total = total + int(myfile.iloc[i,j])
            except:
                ifnull = True
    if ifnull:
        sum.append('null')
    else:
        sum.append(total)
sum1 = {'sum':sum}
sum1 = pd.DataFrame(sum1)
myfile = pd.concat([myfile,sum1],axis=1)
myfile.drop_duplicates()

now = datetime.now()
print(now)

myfile.to_csv('ESCo.csv', index=False)


mylist = myfile[heading[0]].tolist()
right = True
index=[]
for i in range(len(mylist)):
    if i > 0:
        currentTime = datetime.strptime(mylist[i], '%m/%d/%Y %H:%M')
        lastTime = datetime.strptime(mylist[i-1], '%m/%d/%Y %H:%M')
        if currentTime == lastTime + timedelta(minutes=15):
            pass
        else:
            right = False
            index.append(i)
print(right)
print(index)

