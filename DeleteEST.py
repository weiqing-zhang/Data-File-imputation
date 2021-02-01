import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
from datetime import timedelta
# 1. make not 600, but every time change 2. keep colomn A
myfile = pd.read_csv('7143.csv')

heading = myfile.columns.values
mylist = myfile[heading[1]].tolist()
i= 0
MarchList =[]
while i <len(mylist):
    if mylist[i][5:10]== '03-08':
        sublist= mylist[i:]
        left = 672
        if len(sublist)<672:
            left = len(sublist)
        j=0
        while j < left:
            currentdate =  datetime.strptime(mylist[i+j], '%Y-%m-%d %H:%M')
            if currentdate.weekday() != 6:
                j=j+1
            else:
                if currentdate - timedelta(days=7) < datetime.strptime(mylist[i], '%Y-%m-%d %H:%M'):
                    MarchList.append(i+j)
                i = i + 200
                j = j+1000
    else:
        i=i+1


for i in range(len(MarchList)):
    ifright= False
    for j in range(95):
        currenttime = datetime.strptime(mylist[MarchList[i]+j], '%Y-%m-%d %H:%M')
        nexttime = datetime.strptime(mylist[MarchList[i]+j+1], '%Y-%m-%d %H:%M')
        if currenttime == nexttime + timedelta(minutes=45):
            MarchList[i]=MarchList[i]+j+1
            ifright = True
        else:
            pass
    if ifright == False:
        print(ifright)
        print(MarchList[i])

for i in MarchList:
    print(mylist[i])
a = 0

NovList =[]
while a <len(mylist):
    if mylist[a][5:10]== '11-01':
        sublist= mylist[a:]
        left = 672
        if len(sublist)<672:
            left = len(sublist)
        b=0
        while b < left:
            currentdate = datetime.strptime(mylist[a+b], '%Y-%m-%d %H:%M')
            if currentdate.weekday() != 6:
                b=b+1
            else:
                if currentdate - timedelta(days=7) < datetime.strptime(mylist[a], '%Y-%m-%d %H:%M'):
                    NovList.append(a+b)
                a = a + 300
                b = b+3000
    else:
        a=a+1
for i in NovList:
    print(mylist[i])
for i in range(len(NovList)):
    ifright = False
    for j in range(95):
        currenttime = datetime.strptime(mylist[NovList[i]+j], '%Y-%m-%d %H:%M')
        nexttime = datetime.strptime(mylist[NovList[i]+j+1], '%Y-%m-%d %H:%M')
        if currenttime == nexttime - timedelta(minutes=15,hours=1):
            NovList[i]=NovList[i]+j+1
            ifright = True
        else:
            pass
    if ifright == False:
        print(ifright)
        print(MarchList[i])

for i in NovList:
    print(mylist[i])

#for item in MarchList:
    #for i in range(60):
       # myfile.drop(item+12,inplace=True)
       # myfile = myfile.reset_index(drop=True)

if len(MarchList)==0 & len(NovList)== 0:
    pass
elif len(MarchList)==0 & len(NovList)>0:
    start = 0
    end = NovList[0]
    while start < end:
        currentTime = datetime.strptime(mylist[start], '%Y-%m-%d %H:%M')#
        rightTime = currentTime + timedelta(hours=1)
        mylist[start] = rightTime
        start = start + 1
elif MarchList[0] < NovList[0]:
    for i in range(len(MarchList)):
        if i < len(NovList):
            start = MarchList[i]
            end=NovList[i]
            while start<end:
                currentTime= datetime.strptime(mylist[start], '%Y-%m-%d %H:%M')
                rightTime = currentTime + timedelta(hours=1)
                mylist[start] = rightTime
                start=start+1
        else:
            end=len(mylist)
            start = MarchList[i]
            while start<end:
                currentTime= datetime.strptime(mylist[start], '%Y-%m-%d %H:%M')
                rightTime = currentTime + timedelta(hours=1)
                mylist[start] = rightTime
                start=start+1

else:
    start = 0
    end = NovList[0]
    while start < end:
        currentTime = datetime.strptime(mylist[start],'%Y-%m-%d %H:%M')#
        rightTime = currentTime + timedelta(hours=1)
        mylist[start] = rightTime
        start = start + 1
    for i in range(len(MarchList)):
        if i+1 < len(NovList):
            start = MarchList[i]
            end=NovList[i]
            while start<end:
                currentTime= datetime.strptime(mylist[start], '%Y-%m-%d %H:%M')#
                rightTime = currentTime + timedelta(hours=1)
                mylist[start] = rightTime
                start=start+1
        else:
            end=len(mylist)
            start = MarchList[i]
            while start<end:
                currentTime= datetime.strptime(mylist[start],'%Y-%m-%d %H:%M')#
                rightTime = currentTime + timedelta(hours=1)
                mylist[start] = rightTime
                start=start+1

myfile.insert(1,'correctedUTCTime',mylist,True)
myfile.to_csv('7143.csv', index=False)



