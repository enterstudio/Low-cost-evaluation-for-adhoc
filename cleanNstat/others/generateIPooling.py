import getopt,sys
from os.path import isdir, join, isfile
from os import makedirs
import numpy as np

topk=20
qreldir="/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery"
trecdir="/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perquery"
outdir="/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/statAPl/ipoolcwid"
opts, args = getopt.getopt(sys.argv[1:],"j:o:q:r:p:i:a:")
for opt, arg in opts:
    if opt=='-o':
        outdir=str(arg)
    if opt=='-r':
        trecdir=str(arg)
    if opt=='-j':
        qreldir=str(arg)

if not isdir(outdir):
    makedirs(outdir)


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

def incrementalpool(trecf):
    trf=open(trecf,'r')
    poscwids = dict()
    cwidpos = dict()
    for line in trf:
        linearray=line.split()
        pos=int(linearray[3])
        if pos > topk:
            continue
        qid=int(linearray[0])
        cwid=str(linearray[2])
        run=str(linearray[5])
        if cwid not in cwidpos:
            cwidpos[cwid]=list()
        cwidpos[cwid].append(pos)
    cwids=cwidpos.keys()
    trf.close()
    for cwid in cwidpos:
        mpos = min(cwidpos[cwid])
        avepos = sum(cwidpos[cwid]) / float(len(cwidpos[cwid]))
        if mpos not in poscwids:
            poscwids[mpos] = dict()
        if avepos not in poscwids[mpos]:
            poscwids[mpos][avepos]=list()
        poscwids[mpos][avepos].append(cwid)
    return poscwids

######################################################
# output incremental pooling data: in order of cwid
# qid pos rank cwid label avepos
######################################################

poscwids=dict()
cwidjud=dict()
for qid in range(1,301):
    qrelf = join(qreldir, str(qid))
    runf = join(trecdir, str(qid))
    rank = 0
    if isfile(runf):
        poscwids = incrementalpool(runf)
        outf = open(join(outdir, str(qid)), 'w')
        outf.write("#qid pos rank cwid label avepos\n")
    if isfile(qrelf):
        cwidjud = readqrel(qrelf)
    for pos in sorted(poscwids.keys()):
        for avepos in sorted(poscwids[pos].keys()):
            for cwid in poscwids[pos][avepos]:
                label = -2
                rank += 1
                if cwid in cwidjud:
                    label = cwidjud[cwid]
                outlist = [str(qid),str(pos),str(rank), cwid, str(label), '%.4f'%avepos]
                outf.write(' '.join(outlist)+'\n')
    if isfile(runf):
        outf.close()


