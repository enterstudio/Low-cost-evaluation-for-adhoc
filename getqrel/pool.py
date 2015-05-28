import getopt,sys
from os.path import isdir,join
from os import makedirs
from writeqrel import *

topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:o:f:q:n:r:")
for opt, arg in opts:
    if opt=='-o':
        outputdir=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-r':
        trecrunf=str(arg)
    if opt=='-j':
        qrelf=str(arg)

def readtrecrun(runf):
    trf=open(runf,'r')
    runcwids=set()
    for line in trf:
        linearray=line.split()
        pos=int(linearray[3])
        if pos > topk:
            continue
        cwid=str(linearray[2])
        runcwids.add(cwid)
    trf.close()
    return runcwids


# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    for line in qrelF:
        linearray=line.split()
        cwid=linearray[2]
        jud=int(linearray[3])
        cwidjud[cwid]=jud
    qrelF.close()
    return cwidjud


class pooling:
    '''
    selective labeling by pooling method:
    given k, and the trecruns, generate set of documents
    to label by top-k pooling
    init: k, list of docs
    '''
    def __init__(self, runsfqid, k=20):
        # read in missing cwids list
        self.topk = k
        self.trecf = runsfqid
        self.topkcwids = dict()

    def poolDocs(self, pos):
        if len(self.topkcwids) == 0:
            self.trecpool()
        poscwids = self.topkcwids
        L = list()
        for p in sorted(poscwids.keys()):
            if p > pos:
                break
            L.extend(poscwids[p])
        percent = len(L) / float(len(self.cwids))
        return L, percent
    
    def iPoolDocs(self, percent):
        if len(self.topkcwids) == 0:
            self.incrementalpool()
        poscwids = self.topkcwids
        posaccnum = self.posaccnum
        k = round(len(self.cwids) * percent)
        L = list()
        for p in sorted(poscwids.keys()):
            if posaccnum[p] <= k:
                for v in poscwids[p]:
                    L.extend(poscwids[p][v])
            else:
                for v in poscwids[p]:
                    for cwid in poscwids[p][v]:
                        if len(L) >= k:
                            actperc=len(L) / float(len(self.cwids))
                            return L, len(L) / float(len(self.cwids))
                        L.append(cwid)
        actperc=len(L) / float(len(self.cwids))
        return L, actperc
    
    def incrementalpool(self):
        trf=open(self.trecf,'r')
        poscwids = self.topkcwids
        cwidpos=dict()
        for line in trf:
            linearray=line.split()
            pos=int(linearray[3])
            if pos > self.topk:
                continue
            qid=int(linearray[0])
            cwid=str(linearray[2])
            run=str(linearray[5])
            if cwid not in cwidpos:
                cwidpos[cwid]=list()
            cwidpos[cwid].append(pos)
	self.cwids=cwidpos.keys()
        trf.close()
        for cwid in cwidpos:
            mpos = min(cwidpos[cwid])
            avepos = sum(cwidpos[cwid]) / float(len(cwidpos[cwid]))
            if mpos not in poscwids:
                poscwids[mpos] = dict()
            if avepos not in poscwids[mpos]:
                poscwids[mpos][avepos]=list()
            poscwids[mpos][avepos].append(cwid)
        posaccnum = dict()
        accnum = 0
        for pos in sorted(poscwids.keys()):
            for v in poscwids[pos]:
                accnum += len(poscwids[pos][v])
            posaccnum[pos] = accnum
        self.posaccnum = posaccnum
    
    # pos-(cwids)
    def trecpool(self):
        trf=open(self.trecf,'r')
        poscwids = self.topkcwids
        cwidpos=dict()
        for line in trf:
            linearray=line.split()
            pos=int(linearray[3])
            if pos > self.topk:
                continue
            qid=int(linearray[0])
            cwid=str(linearray[2])
            run=str(linearray[5])
            if cwid not in cwidpos:
                cwidpos[cwid]=list()
            cwidpos[cwid].append(pos)
	self.cwids=cwidpos.keys()
        trf.close()
        for cwid in cwidpos:
            mpos=min(cwidpos[cwid])
            if mpos not in poscwids:
                poscwids[mpos] = set()
            poscwids[mpos].add(cwid)


percents=[0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]

if not isdir(outputdir):
    makedirs(outputdir)
runcwids = readtrecrun(trecrunf)
docs=list(runcwids)
cwidjud=readqrel(qrelf)
tpool=pooling(trecrunf)
ipool=pooling(trecrunf)
for percent in percents:
    outdir = join(outputdir, 'incrementalpool','qrels',str(percent))
    if not isdir(outdir):
        makedirs(outdir)
    outbqrel=open(join(outdir, str(qid) + ".bqrel"),'w')
    outoqrel=open(join(outdir, str(qid) + ".oqrel"),'w')
    L, actperc =ipool.iPoolDocs(percent)
    outbqrel.write(bqrel(qid,L,cwidjud,docs))
    outoqrel.write(oqrel(qid,L,cwidjud,docs))
    outbqrel.close()
    outoqrel.close()
for pos in range(1,21):
    outdir = join(outputdir, 'trecpool','qrels',str(pos))
    if not isdir(outdir):
        makedirs(outdir)
    outbqrel=open(join(outdir, str(qid) + ".bqrel"),'w')
    outoqrel=open(join(outdir, str(qid) + ".oqrel"),'w')
    L, actperc =tpool.poolDocs(pos)
    outbqrel.write(bqrel(qid,L,cwidjud,docs))
    outoqrel.write(oqrel(qid,L,cwidjud,docs))
    outbqrel.close()
    outoqrel.close()
