import getopt,sys

topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:f:q:r:")
for opt, arg in opts:
    if opt=='-f':
        trainf=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-j':
        qrelf=str(arg)
    if opt=='-r':
        trecrunf=str(arg)

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
        if jud == -2:
            continue
        cwid=linearray[2]
        cwidjud[cwid]=jud
    qrelF.close()
    return cwidjud

# input format:  
# cwid label {term:fvalue}
# output format:
# cwid-{term:tf-idf}
def tfidffeatures(featurefile):
    features=open(featurefile,'r')
    cwids=set()
    result={}
    for line in features:
        linearray=line.split()
        if len(linearray) > 2:
            cwid=linearray[0]
            result[cwid]=dict()
            for i in range(1, len(linearray)):
                termtfidf=linearray[i].split(':')
                if len(termtfidf) == 2:
                    if len(termtfidf[0]) >=1:
                        if not termtfidf[0].replace('.','',1).isdigit():
                            result[cwid][termtfidf[0]]=float(termtfidf[1])
    features.close()
    return result

######################################################
# read in the data
######################################################
# read in tf-idf feature
features = tfidffeatures(trainf)
# read in selected qrel qid-[cwids]
cwidjud = readqrel(qrelf)
# read in trecruns
rcwid, docsysrank = readtrecrun(trecrunf)
# intereaction of different sources' cwid
fcwid = set(features.keys())
qcwid = set(cwidjud.keys())

qrcwid=set.intersection(qcwid, rcwid)

diffcwid = qrcwid - fcwid
missingrate = len(diffcwid) / float(len(qrcwid))

print qid, len(diffcwid), len(qrcwid), '%d%%'%(missingrate*100)
