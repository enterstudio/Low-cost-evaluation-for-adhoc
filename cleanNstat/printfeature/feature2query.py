import getopt,sys
from os.path import join

topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:f:q:o:")
for opt, arg in opts:
    if opt=='-f':
        trainf=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-j':
        qrelf=str(arg)
    if opt=='-o':
        outdir=str(arg)

def readtrecrun(runf):
    trf=open(runf,'r')
    runcwids=set()
    cwidsysrank=dict()
    for line in trf:
        linearray=line.split()
        pos=int(linearray[3])
        if pos > topk:
            continue
        cwid=str(linearray[2])
        runname=str(linearray[5])
        runcwids.add(cwid)
        if cwid not in cwidsysrank:
            cwidsysrank[cwid]=dict()
        cwidsysrank[cwid][runname]=pos
    trf.close()
    return runcwids, cwidsysrank

# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    for line in qrelF:
        linearray=line.split()
        jud=int(linearray[3])
        cwid=linearray[2]
        cwidjud[cwid]=jud
    qrelF.close()
    return cwidjud

# input format:  
# cwid label {term:fvalue}
# output format:
# cwid-{term:tf-idf}
def tfidffeatures(featurefile, cwids):
    outf = open(join(outdir, str(qid)), "w")
    features=open(featurefile,'r')
    for line in features:
        linearray=line.split()
        if len(linearray) >= 1:
            cwid=linearray[0]
            if cwid in cwids:
                outf.write(line)
    features.close()
    outf.close()

######################################################
# read in the data
######################################################
# read in selected qrel qid-[cwids]
cwidjud = readqrel(qrelf)
# read in tf-idf feature
tfidffeatures(trainf, set(cwidjud.keys()))
