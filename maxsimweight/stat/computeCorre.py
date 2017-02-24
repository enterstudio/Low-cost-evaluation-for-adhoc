from scipy.stats import kendalltau, pearsonr
import getopt,sys
from copy import deepcopy
from os.path import basename
import re

opts,args=getopt.getopt(sys.argv[1:],'o:x:t:n:l:',["originalqrel=","partialqrelrunx=","partialqrelruny=","tauname=","expname="])
correM='tau'
delimiter=' '
for opt,arg in opts:
    if opt in ('-o','--originalqrel'):
        oqrelr=str(arg)
    elif opt in ('-x','--paritialqrelrunx'):
        xpqrelr=str(arg)
    elif opt in ('-t','--tauname'):
        correM=str(arg)
    elif opt in ('-n','--expname'):
        expname=str(arg)
    elif opt in ('-l'):
        delimiter=str(arg)

#print 'input parameters:',oqrelr,pqrelr,correM

# read in the tmp measure score file
# runid,erria,alphandcg,nrbp,srecall
scores={}
colnum=0
#indexmap={'ndcg20':0,'err20':1,'map':2,'p20':3,'r20':4}
#mnames=['ndcg20','err20','map','p20','r20']
indexmap={'ndcg20':0,'map':1}
mnames=['ndcg20','map']
# runname, measures....
for line in open(oqrelr):
   linearray=line.split(delimiter)
   colnum=len(linearray)
   runid=linearray[0]
   measures=linearray[1:]
   if runid not in scores:
       # 0,1 groups
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


def getCorrespondingList(dictionary, measure):
    index=indexmap[measure]
    first=[]
    second=[]
    for runid in dictionary.keys():
        first.append(float(dictionary[runid][0][index]))
        second.append(float(dictionary[runid][1][index]))
    return first,second


measureCorr=[1]*len(measures)
for i in range(0, len(mnames)):
    mname = mnames[i]
    completeScore,xpartialScore=getCorrespondingList(scores,mname)
    xtau,xpvaluet =kendalltau(completeScore,xpartialScore)
    xr, xpvaluer =pearsonr(completeScore,xpartialScore)
    measureCorr[mnames.index(mname)] = '%0.4f'%xtau+' '+'%0.4f'%xr

print expname," ".join(measureCorr)

