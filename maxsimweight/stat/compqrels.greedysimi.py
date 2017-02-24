from basicfunc import *
import numpy as np
from os.path import basename,join
from os import listdir,walk
import sys

weightname = sys.argv[1]
kernel = sys.argv[2]

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



def compqrels(fqrel,pqrel):
    frelq, firrelq, ffullq, fqids = qrelrelirrel(fqrel)
    prelq, pirrelq, pfullq, pqids = qrelrelirrel(pqrel)
    qidMiss={}
    qidPrec={}
    qidReca={}
    for qid in ffullq:
        if qid >150:
            continue
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        miss = 0
        for cwid in ffullq[qid]:
            if qid not in pfullq:
                miss += 1
                continue
            if cwid not in pfullq[qid]:
                miss += 1
                continue
            TP += int((cwid in prelq[qid]) and (cwid in frelq[qid]))
            TN += int((cwid in pirrelq[qid]) and (cwid in firrelq[qid]))
            FP += int((cwid in prelq[qid]) and (cwid in firrelq[qid]))
            FN += int((cwid in pirrelq[qid]) and (cwid in frelq[qid]))
        qidMiss[qid]=miss/float(len(ffullq[qid]))
        qidPrec[qid]=(TP/float(TP+FP) if (TP+FP) > 0 else 0)
        qidReca[qid]=(TP/float(TP+FN) if (TP+FN) > 0 else 0)
    missrate = np.mean(qidMiss.values())
    precision = np.mean(qidPrec.values())
    recall = np.mean(qidReca.values())
    f1 = 2 * (precision * recall) / float(precision + recall)
    #resstr = ['%.4f'%f1, '%.4f'%precision, '%.4f'%recall,'%.1f%%'%(missrate*100)]
    return f1,missrate

qreldir="/scratch/GW/pool0/khui/result/2stagelowcost/GreedySimi"
fullqrel="/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wtf"
outputf=  qreldir +  "/_comp.measure.summary." + kernel + "-" + weightname 
outf=open(outputf,'w')

thresPercQrel=dict()
for root, dirs, files in walk(qreldir):
    if len(root.split("/")) != 12:
        continue
    for f in files:
        if f.endswith("qrel"):
            perc = float(root.split("/")[-1])
            threshold = root.split("/")[-3]
            if root.split("/")[-2] != weightname or  root.split("/")[-4] != kernel:
                continue
            if threshold not in thresPercQrel:
                thresPercQrel[threshold] = dict()
            if perc not in thresPercQrel[threshold]:
                thresPercQrel[threshold][perc]=dict()
            thresPercQrel[threshold][perc]=root

for threshold in sorted(thresPercQrel.keys()):
    outf.write('# ' + kernel +" " +weightname +" "+ str(threshold) + "\n")
    for perc in sorted(thresPercQrel[threshold].keys()):
        f1, missrate=compqrels(fullqrel, thresPercQrel[threshold][perc])
        resultstr=['%.2f'%perc,'%.4f'%f1,'%.1f%%'%((1-missrate)*100),'\n']
        outf.write(' '.join(resultstr))
        outf.flush()
    outf.write("\n\n\n")
outf.close()
print "compqrel finished!"
