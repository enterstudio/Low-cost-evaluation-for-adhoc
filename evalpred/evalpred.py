import getopt,sys
import numpy as np
from os.path import basename,join
from os import listdir,walk
import sys

topk=20
opts, args = getopt.getopt(sys.argv[1:],"f:q:")
for opt, arg in opts:
    if opt=='-q':
        qreldir=str(arg)
    if opt=='-f':
        fullqrel=str(arg)

measures=['TP', 'TN', 'FP', 'FN', 'missrate', 'precision', 'recall', 'f1']
def stat(qidV):
    measures=qidV.values()
    lmeasures = [v for v in measures if v >= 0]
    length=len(lmeasures)
    validrespercent = length / float(len(measures))
    if sum(lmeasures) == length:
        return np.array([1,1]),1,np.array([1,1]),validrespercent
    if length > 1:
        n, min_max, mean, var, skew, kurt = stats.describe(lmeasures)
        left_right = stats.t.interval(0.95,length-1 ,loc=mean, scale=math.sqrt(var/length))
        return min_max,mean,left_right,validrespercent
    elif length == 1:
        return np.array([lmeasures[0],lmeasures[0]]),lmeasures[0],np.array([lmeasures[0],lmeasures[0]])\
                ,validrespercent
    else:
        return np.array([0,0]),0,np.array([0,0]),validrespercent

# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    first = True
    for line in qrelF:
        linearray=line.split()
        if first:
            qid=int(linearray[0])
            first = False
        jud=int(linearray[3])
        if jud > 0:
            jud = 1
        elif jud == -2:
            jud = -2
        else:
            jud = 0
        cwid=linearray[2]
        cwidjud[cwid]=jud
    qrelF.close()
    return qid, cwidjud

# {cwid:jud}
def readfqrel(qrelf, qidcwidjud):
    qrelF=open(qrelf,'r')
    for line in qrelF:
        linearray=line.split()
        qid=int(linearray[0])
        jud=int(linearray[3])
        if jud > 0:
            jud = 1
        elif jud == -2:
            jud = -2
        else:
            jud = 0
        cwid=linearray[2]
        if qid not in qidcwidjud:
            qidcwidjud[qid]=dict()
        qidcwidjud[qid][cwid]=jud
    qrelF.close()

def compqrels(fcwidjud,pcwidjud):
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    miss = 0
    for cwid in pcwidjud:
        pjud = pcwidjud[cwid]
        fjud = fcwidjud[cwid]
        TP += int((pjud == 1) and (fjud == 1))
        TN += int((pjud == 0) and (fjud == 0))
        FP += int((pjud == 1) and (fjud == 0))
        FN += int((pjud == 0) and (fjud == 1))
        miss += int((pjud == -2) and (fjud != -2))
    missrate = miss / float(len(pcwidjud))
    precision = (TP/float(TP+FP) if (TP+FP) > 0 else 0)
    recall = (TP/float(TP+FN) if (TP+FN) > 0 else 0)
    if (precision + recall) != 0:
        f1 = 2 * (precision * recall) / float(precision + recall)
    else:
        f1 = 0
    measureval = dict()
    measureval['TP'] = TP
    measureval['TN'] = TN
    measureval['FP'] = FP
    measureval['FN'] = FN
    measureval['missrate'] = missrate
    measureval['precision'] = precision
    measureval['recall'] = recall
    measureval['f1'] = f1
    return measureval


qidcwidjud=dict()
for year in ['09','10','11','12']:
    readfqrel(fullqrel + year,qidcwidjud)

mnameyqidval = dict()
for mname in measures:
    mnameyqidval[mname] = dict()
    for year in ['09','10','11','12']:
        mnameyqidval[mname][year] = dict()
for f in listdir(qreldir):
    if not f.endswith('pqrel'):
        continue
    qid, pcwidjud = readqrel(join(qreldir,f))
    measureval = compqrels(qidcwidjud[qid], pcwidjud)
    for mname in measureval:
        if qid < 51:
            year = '09'
        elif qid < 101:
            year = '10'
        elif qid < 151:
            year = '11'
        elif qid < 201:
            year = '12'
        mnameyqidval[mname][year][qid] = measureval[mname]

outstr=list()
headline=['#']
headline.extend(measures)
outstr.append(' '.join(headline))
for year in ['09','10','11','12']:
    TP=np.mean(mnameyqidval['TP'][year].values())
    TN=np.mean(mnameyqidval['TN'][year].values())
    FP=np.mean(mnameyqidval['FP'][year].values())
    FN=np.mean(mnameyqidval['FN'][year].values())
    missrate=np.mean(mnameyqidval['missrate'][year].values())
    precision=np.mean(mnameyqidval['precision'][year].values())
    recall=np.mean(mnameyqidval['recall'][year].values())
    f1=np.mean(mnameyqidval['f1'][year].values())
    yearstr = [year,'%.4f'%TP,'%.4f'%TN,'%.4f'%FP,'%.4f'%FN,\
            '%.4f'%missrate, '%.4f'%precision, '%.4f'%recall,'%.4f'%f1]
    outstr.append(' '.join(yearstr))
print '\\n'.join(outstr)
