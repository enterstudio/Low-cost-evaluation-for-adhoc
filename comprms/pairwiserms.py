from sklearn.metrics import mean_squared_error as mse
from math import sqrt
import getopt,sys
from copy import deepcopy
from os.path import basename
import re

opts,args=getopt.getopt(sys.argv[1:],'o:x:l:',["originalqrel=","partialqrelrunx=","partialqrelruny=","tauname=","expname="])
correM='tau'
delimiter=' '
for opt,arg in opts:
    if opt in ('-o','--originalqrel'):
        oqrelr=str(arg)
    elif opt in ('-x','--paritialqrelrunx'):
        xpqrelr=str(arg)
    elif opt in ('-l'):
        delimiter=str(arg)


# read in the measure score file
# runid,erria,alphandcg,nrbp,srecall
scores={}
colnum=0
# runname, measures....
for line in open(oqrelr):
   linearray=line.split(delimiter)
   colnum=len(linearray)
   runid=linearray[0]
   measures=linearray[1:]
   if runid not in scores:
       scores[runid]=[[],[]]
   scores[runid][0]=deepcopy(measures)
for line in open(xpqrelr):
    linearray=line.split(delimiter)
    if colnum != len(linearray):
        continue
    runid=linearray[0]
    measures=linearray[1:]
    if runid in scores:
        scores[runid][1]=deepcopy(measures)


def getCorrespondingList(dictionary, measureid):
    first=[]
    second=[]
    for runid in dictionary.keys():
        if len(dictionary[runid][1]) > 0:
            first.append(float(dictionary[runid][0][measureid]))
            second.append(float(dictionary[runid][1][measureid]))
    return first,second


measureCorr=[1]*(colnum - 1)
for i in range(colnum - 1):
    x, y=getCorrespondingList(scores,i)
    rmse = sqrt(mse(x, y))
    measureCorr[i] = '%0.4f'%rmse

print " ".join(measureCorr)

