from basicfunc import *
import numpy as np
from os.path import basename,join
from os import listdir,walk


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

qreldir="/scratch/GW/pool0/khui/result/2stagelowcost/GreedySimi/qrelcorr"
fullqrel="/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wtf"
outputf=qreldir + "/qrelcorr.summary"
outf=open(outputf,'w')

gnPercQrel=dict()
gnPercQrelB=dict()
for year in ['09','10','11','12']:
    direc=qreldir + "/" + year
    for f in listdir(direc):
        for line in open(join(direc,f)):
            cols=line.split()
            if len(cols) == 6:
                #year=int(cols[0].split('-')[0])
                wn=str(cols[0].split('-')[2])
                threshold=float(cols[0].split('-')[3])
                perc=float(cols[0].split('-')[4])
                kernel=str(cols[0].split('-')[1])
                if kernel == "linear":
                    continue
                if wn == "entropy" or wn == "srk":
                    continue
                if threshold != 0:
                    continue
                gn = "-".join([kernel,wn,str(threshold)])
                if gn not in gnPercQrel:
                    gnPercQrel[gn]=dict()
                    gnPercQrelB[gn]=dict()
                if perc not in gnPercQrel[gn]:
                    gnPercQrel[gn][perc]=dict()
                    gnPercQrelB[gn][perc]=dict()
                    gnPercQrel[gn][perc]['err20']=dict()
                    gnPercQrel[gn][perc]['map']=dict()
                    gnPercQrelB[gn][perc]['err20']=dict()
                    gnPercQrelB[gn][perc]['map']=dict()
                if cols[1] == 'orig':
                    gnPercQrel[gn][perc]['err20']=float(cols[2])
                    gnPercQrel[gn][perc]['map']=float(cols[4])
                elif cols[1] == 'origbin':
                    gnPercQrelB[gn][perc]['err20']=float(cols[2])
                    gnPercQrelB[gn][perc]['map']=float(cols[4])

    for gn in sorted(gnPercQrel.keys()):
        outf.write("# " +str(year) + " " + gn + " original qrel: err20 map kendall\'s tau\n")
        for perc in sorted(gnPercQrel[gn].keys()):
            resultstr=['%.2f'%perc,\
                    '%.4f'%gnPercQrel[gn][perc]['err20'],'%.4f'%gnPercQrel[gn][perc]['map'],'\n']
            outf.write(' '.join(resultstr))
            outf.flush()
        outf.write("\n\n\n")
#    for gn in sorted(gnPercQrelB.keys()):
#        outf.write("# " +str(year) + " "+gn+" binary qrel: err20 map kendall\'s tau\n")
#        for perc in sorted(gnPercQrelB[gn].keys()):
#            resultstr=['%.2f'%perc,\
#            '%.4f'%gnPercQrelB[gn][perc]['err20'],'%.4f'%gnPercQrelB[gn][perc]['map'],'\n']
#            outf.write(' '.join(resultstr))
#            outf.flush()
#        outf.write("\n\n\n")
outf.close()
print "compqrel finished!"
