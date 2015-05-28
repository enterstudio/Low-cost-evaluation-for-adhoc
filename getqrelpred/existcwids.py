from os import makedirs
from os.path import join, isdir
import sys,getopt
from random import sample
from writeqrel import *


repeattime=30
topk=20
#parsing arguments
opts, args = getopt.getopt(sys.argv[1:],"q:i:j:")
for opt, arg in opts:
    if opt=='-q':
        qid=int(arg)
    if opt=='-i':
        intf=str(arg)
    if opt=='-j':
        qrelf=str(arg)

# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    cwidline=dict()
    for line in qrelF:
        linearray=line.split()
        cwid=linearray[2]
        jud=int(linearray[3])
        cwidjud[cwid]=jud
        cwidline[cwid]=line
    qrelF.close()
    return cwidjud, cwidline

# {cwid:jud}
def readexistqrel(qrelf, cwidjud, cwidline):
    qrelF=open(qrelf,'r')
    cwids=set()
    mcwidline=dict()
    ocwidline=dict()
    bcwidline=dict()
    for line in qrelF:
        linearray=line.split()
        cwid=linearray[2]
        jud=int(linearray[3])
        if jud == -2:
            mcwidline[cwid]=line.rstrip()
        else:
            jud = cwidjud[cwid]
            ocwidline[cwid]=cwidline[cwid].rstrip()
            if jud > 0:
                bcwidline[cwid]=' '.join([str(qid),str(0),cwid, str(1)])
            else:
                bcwidline[cwid]=' '.join([str(qid),str(0),cwid, str(0)])
    return mcwidline, ocwidline, bcwidline

cwidjud, cwidline = readqrel(qrelf)
mcwidline, ocwidline, bcwidline = readexistqrel(intf + ".bqrel", cwidjud, cwidline)
#os.remove(intf + ".bqrel")
#os.remove(intf + ".oqrel")
ooutlist=mcwidline.values() + ocwidline.values()
boutlist=mcwidline.values()+ bcwidline.values()
ooutf=open(intf + ".oqrel",'w')
boutf=open(intf + ".bqrel",'w')

ooutf.write('\n'.join(ooutlist))
boutf.write('\n'.join(boutlist))
ooutf.close()
boutf.close()

