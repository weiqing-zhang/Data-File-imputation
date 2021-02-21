import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
from datetime import timedelta
# 1. make not 600, but every time change 2. keep colomn A
myfile = pd.read_csv('7143.csv')

heading = myfile.columns.values
#mylist is the list of time interval
mylist = myfile[heading[1]].tolist()
i= 0
# MarchList is the list of Sunday of March 8th each year, which is the day that time shift occurs
MarchList =[]
while i <len(mylist):
    # the week of March 8th is time when time zone shift occur
    if mylist[i][5:10]== '03-08':
        sublist= mylist[i:]
        # there are 672 time intervals in a week
        left = 672
        # each sublist checks a week of time after March 8th. If the data is not long enough, then get as far as we have. 
        if len(sublist)<672:
            left = len(sublist)
        j=0
        while j < left:
            #change the time format
            currentdate =  datetime.strptime(mylist[i+j], '%Y-%m-%d %H:%M')
            #find the Sunday in the week of March 8th
            if currentdate.weekday() != 6:
                j=j+1
            else:
                if currentdate - timedelta(days=7) < datetime.strptime(mylist[i], '%Y-%m-%d %H:%M'):
                    MarchList.append(i+j)
                # 200 doesn't have a meaning, but it is large enough so that the code will check the March 8th of the following year
                i = i + 200
                # make j large enough to pause
                j = j+1000
    else:
        i=i+1


for i in range(len(MarchList)):
    ifright= False
    for j in range(95):
        #change the time format
        currenttime = datetime.strptime(mylist[MarchList[i]+j], '%Y-%m-%d %H:%M')
        nexttime = datetime.strptime(mylist[MarchList[i]+j+1], '%Y-%m-%d %H:%M')
        #time shift is an hour, so the interval when that happens will have a gap of 45min
        if currenttime == nexttime + timedelta(minutes=45):
            MarchList[i]=MarchList[i]+j+1
            ifright = True
        else:
            pass
    #return the time interval if no time shift found
    if ifright == False:
        print(ifright)
        print(MarchList[i])

for i in MarchList:
    print(mylist[i])
a = 0
# Nov list contains the fist Sunday in Novemeber, when the winter time shift occurs. It is the same as the previous function. (But minus 45 min because that day get shorter)
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

# adjust time depends on different conditions (whether the winter time or summer time zone comes first)
if len(MarchList)==0 & len(NovList)== 0:
    pass
#add one hour during summer time zone when winter time comes first
elif len(MarchList)==0 & len(NovList)>0:
    start = 0
    end = NovList[0]
    while start < end:
        currentTime = datetime.strptime(mylist[start], '%Y-%m-%d %H:%M')#
        rightTime = currentTime + timedelta(hours=1)
        mylist[start] = rightTime
        start = start + 1
#change the time interval when summer time shift comes first
#add one hour to summer time zone
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
#when winter time shift comes first, still add one hour to summer time zone
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



