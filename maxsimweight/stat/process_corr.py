from os import listdir
import os
from os.path import join
import numpy as np

year=str(os.sys.argv[1])
corredir="/scratch/GW/pool0/khui/result/2stagelowcost/corr/msimThreshold/"+str(year)
#"/scratch/GW/pool0/khui/result/2stagelowcost/corr/pool/"+str(year)

def poolcorr(line):
    cols = line.split()
    pos = float(cols[0].split('-')[-1])
    sn = cols[0].split('-')[0]
    fn = cols[0].split('-')[1]
    mln = cols[0].split('-')[2]
    qreln = cols[1]
    errK=float(cols[2])
    errP=float(cols[3])
    mapK=float(cols[4])
    mapP=float(cols[5])
    return sn,fn,mln,pos,qreln,errK,errP,mapK,mapP
    
def msimwcorr(line):
    cols = line.split()
    pos = float(cols[0].split('-')[-1])
    sn = cols[0].split('-')[0]
    fn = cols[0].split('-')[1]
    wn = cols[0].split('-')[2]
    mln = cols[0].split('-')[3]
    qreln = cols[1]
    errK=float(cols[2])
    errP=float(cols[3])
    mapK=float(cols[4])
    mapP=float(cols[5])
    return sn,fn,wn, mln,pos,qreln,errK,errP,mapK,mapP

def poolperc():
    if year == "09":
        qmin=1
        qmax=50
    elif year == "10":
        qmin=51
        qmax=100
    elif year == "11":
        qmin=101
        qmax=150
    elif year == "12":
        qmin=151
        qmax=200
    percf="/scratch/GW/pool0/khui/result/2stagelowcost/fusion.pool/f-tfidf/_posperc"
    posPerc=dict()
    perclist=dict()
    for line in open(percf):
        cols=line.split()
        qid = int(cols[0])
        if qid > qmax or qid < qmin:
            continue
        pos=int(cols[1])
        perc=float(cols[2])
        if pos not in posPerc:
            posPerc[pos] = list()
        posPerc[pos].append(perc)
    for pos in posPerc.keys():
        perclist[pos]=(np.mean(posPerc[pos]))
    return perclist


poolperc=poolperc()
# (ndcg-kentall, map-kentall, ndcg-pearson, map-pearson) X (orig, binary)
percCorr=dict()
for f in listdir(corredir):
    for line in open(join(corredir, f)):
        sn,fn,mln,perc,qrel,errK,errP,mapK,mapP = poolcorr(line)
        percCorr[perc]=[errK,mapK,errP,mapP]

print '#',year,'errK,mapK,errP,mapP'
for perc in sorted(percCorr.keys()):
    print '%.2f'%perc, ' '.join(['%.4f'%x for x in percCorr[perc]])

print '\n\n\n'






'''

if qrel=="origbin":
            continue
        if mln == "ridge":
            continue
        if wn not in ['sysrr','sysrn']:
            continue
        if '-'.join((sn,fn)) not in ['tfsysSim-tfs','tfidfSim-tf']:
            continue

        fswn = "-".join((sn,fn,wn,mln))
        if fswn not in fnsnwnCorr:
            fnsnwnCorr[fswn]=dict()
        fnsnwnCorr[fswn][perc]=[errK,mapK,errP,mapP]
print '#',year,'errK,mapK,errP,mapP'
for fswn in sorted(fnsnwnCorr.keys()):
    print '#',fswn
    for perc in sorted(fnsnwnCorr[fswn].keys()):
        print '%.2f'%perc, ' '.join(['%.4f'%x for x in fnsnwnCorr[fswn][perc]])
    print '\n\n\n'



fswnMcorr=dict()
for fswn in fnsnwnCorr.keys():
    mc = np.mean(fnsnwnCorr[fswn])
    if mc in fswnMcorr:
        print fswn,fswnMcorr[np.mean(fnsnwnCorr[fswn])],'%.4f'%mc
    fswnMcorr[np.mean(fnsnwnCorr[fswn])]=fswn
count=1
for mc in sorted(fswnMcorr.keys(),reverse=True):
    if count >8:
        break
    print fswnMcorr[mc],'%.4f'%mc
    count=count+1
'''

